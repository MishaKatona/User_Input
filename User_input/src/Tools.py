from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QFrame
from PySide6.QtGui import QColor, QPalette
from functools import reduce
import operator
from copy import deepcopy
import json
import toml


def create_widget_boxlayout(layout: str = "Vertical",
                            padding: list = [0, 0, 0, 0]):
    """Convenient function to generate BoxLayout with padding"""
    frame = QWidget()

    if layout == "Vertical":
        layout = QVBoxLayout()
    elif layout == "Horizontal":
        layout = QHBoxLayout()
    elif layout == "Grid":
        layout = QGridLayout()
    else:
        raise ValueError(f"{layout} not valid, please use; Horizontal, "
                         f"Vertical, Grid")

    frame.setContentsMargins(0, 0, 0, 0)
    layout.setContentsMargins(*padding)
    frame.setLayout(layout)

    return frame, layout


def merge_templates(default: dict, template_lst: list, logger) -> dict:
    """Merges provided templates with priority low -> high with missing
    values being pulled form default"""
    final_templates = {}
    # Loop over each template dict
    for template_dict in template_lst:
        # Loop over each individual template defined in the dictionary
        for key, template in template_dict.items():
            # If current template is new use default
            if key not in final_templates:
                final_templates[key] = deepcopy(default)

            if not template:
                logger.warning(f"Template with key {key} evaluates to False, "
                               f"please either remove the key or define it")
                continue

            # update each sub_key
            for sub_key, definition in template.items():
                prev_sub_key = final_templates[key][sub_key]
                final_templates[key][sub_key] = update_component(sub_key,
                                                                 prev_sub_key,
                                                                 template[sub_key],
                                                                 default[sub_key])
    return final_templates


def update_component(component: dict, target: dict,
                     updater: dict, default: dict) -> dict:
    # Since Args in Body is a nested dict, I need to treat it differently
    args = None
    if component == "Body" and updater and "Args" in updater:
        args = updater["Args"]

    target = update(target, updater, default)

    if args is not None:
        target["Args"] = args

    return target


def update(target: dict, updater: dict, default: dict) -> dict:
    # If component is explicitly disabled
    if not updater:
        return False
    # If component is defined for first time, use default template
    elif not target and updater:
        target = default.copy()
        target.update(updater)
        return target
    # If both are dictionaries do normal update
    else:
        target.update(updater)
        return target


def flatten(nested_dict: dict,
            depth: int,
            inject_metadata: bool = False,
            parent=[]) -> dict[str, dict]:
    """Flattens nested_dict recursively down till the specified depth
    Inputs:
        - nested_dict: dictionary to (partially) flatten
        - depth: to what depth it should flatten
        - inject_metadata: inserts a metadata dictionary with path, pathstr, name
        - parent: needed for recursive (used to store the hierarchy)"""
    flat_dict = {}
    for name, val in nested_dict.items():
        if depth != 0:
            flat_dict.update(flatten(nested_dict=val,
                                     depth=depth - 1,
                                     inject_metadata=inject_metadata,
                                     parent=parent + [name]))
        else:
            path = parent + [name]
            if inject_metadata:
                metadata = {"Path": path,
                            "PathStr": "_".join(path),
                            "Name": path[-1]}
                val["MetaData"] = metadata
            flat_dict["_".join(path)] = val

    return flat_dict


def get_by_path(root: dict, items: list):
    """Access a nested object in root by item sequence."""
    return reduce(operator.getitem, items, root)


def nest(values: dict, paths: dict) -> dict:
    """Takes a flat dict of values and converts it back to a nested format
    Inputs:
        - values: flat dictionary with key value pairs
        - paths: has the same key"""
    master = {}
    for key, path in paths.items():
        for idx, path_key in enumerate(path):
            path_lst = path[:idx]
            dic = get_by_path(master, path_lst)
            if path_key not in dic:
                if idx != len(path) - 1:
                    dic[path[idx]] = {}
                else:
                    dic[path[idx]] = values[key]
    return master


def merger_dictionaries(dict_list: list[dict]) -> dict:
    """
    Takes the list of dictionaries and generates a master dictionary by
    updating all keys and values from each dictionary in the list with the
    priority going from low->high (last dict overwrites everything)
    """
    master_dict = {}
    for dictionary in dict_list:
        if master_dict:
            master_dict = master_dict.update(dictionary)
        else:
            master_dict = dictionary

    return master_dict


class QHLine(QFrame):
    def __init__(self, width=1, rgb=(80, 80, 80)):
        super(QHLine, self).__init__()
        self.setFrameShape(QFrame.HLine)
        self.setFrameShadow(QFrame.Plain)
        self.setLineWidth(width)
        pal = self.palette()
        pal.setColor(QPalette.WindowText, QColor(*rgb))
        self.setPalette(pal)


def load_dict_like_resource(resource, default=None) -> [dict, str]:
    """Returns the dict resource along with the path it came from"""
    resource_type = type(resource)

    if resource_type == dict:
        return resource, None

    elif resource_type == str:
        suffix = resource.split(".")[-1]

        with open(resource, "r") as file:
            if suffix == "json":
                return json.loads(file.read())
            elif suffix == "toml":
                return toml.loads(file.read())
            else:
                print(f"Invalid file extension .{suffix}, "
                      f"only json, or toml can be used")

    elif resource is None:
        return default, None

    return None, None


def dump_dict_resource(resource, resource_path):
    if type(resource) != dict:
        print("resource not a dict")
        return False

    suffix = resource_path.split(".")[-1]

    with open(resource_path, "w") as file:
        if suffix == "json":
            serialized = json.dumps(resource, indent=4)
        elif suffix == "toml":
            serialized = toml.dumps(resource)
        else:
            print(f"Invalid file extension .{suffix}, "
                  f"only json, or toml can be used.")
            return False
        file.write(serialized)
        return True
