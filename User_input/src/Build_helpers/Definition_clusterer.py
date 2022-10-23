# format settings {"TabBy": "Tab", "GroupBy": "Group",
#                  "DefaultTab": "default"}


class ClusterDefinitions:

    def __init__(self,
                 definitions: dict,
                 cluster_settings: dict,
                 logger):

        self.definitions = definitions
        self.settings = cluster_settings
        self.logger = logger

        self.verify_settings()
        self.assign_tab()
        self.assign_group()
        self.assign_sub_setting()

    def get_definitions(self):
        return self.definitions

    def verify_settings(self):
        # Get the depth (len) of the path
        depth = len(next(iter(self.definitions.values()))["MetaData"]["Path"]) - 1
        sett = self.settings
        tab_by, group_by = sett["TabBy"], sett["GroupBy"]
        # If tabbing level is lower than what is available reset to default
        if type(tab_by) == int and tab_by >= depth:
            self.logger.info(f"Cannot tab by that level, falling back to Tab")
            self.settings["TabBy"] = "Tab"

        # If grouping level is lower that available, or higher than tab level,
        # set back to default
        if type(group_by) == int:
            if group_by >= depth or (type(tab_by) == int and group_by <= tab_by):
                self.logger.info(f"Cannot group by that level, falling back to Group")
                self.settings["GroupBy"] = "Group"


    def find_element(self, self_path: list, name_to_find: str, search_type: str):
        """Returns None if not found, returns False if could not resolve,
        returns the path list if it found it"""
        path_str = "_".join(self_path)

        options = []
        for key, definition in self.definitions.items():
            if definition["MetaData"]["Name"] == name_to_find:
                options.append(definition["MetaData"]["Path"])

        # If element not found
        if not options:
            # If it is a group its ok if it does not exist
            if search_type == "Group":
                return None
            self.warn(key=path_str,
                      logger_str=f"{search_type} {name_to_find} defined by "
                                 f"{path_str} does not exist",
                      issue_str=f"{search_type} {name_to_find} does not exist")

            return None
        # If the element to be found is unique
        elif len(options) == 1:
            return options[0]

        # If there are more than 1 elements with the given name
        # Loop over each path level and get the "closest" matching one
        # (its -2 because of len vs idx thing, and because I dont want to match names)
        depth = 0
        while depth < len(self_path) - 1:
            # As it reached this step there has to be more than 1,
            # so we start eliminating ones that are "further" away,
            # if non stay that means that the same level had multiple ==> cannot resolve
            options = [o for o in options if o[depth] == self_path[depth]]
            depth += 1

            if len(options) == 1:
                return options[0]
            elif len(options) == 0:
                break

        # Multiple candidates at a given level => cannot resole which one
        self.warn(key=path_str,
                  logger_str=f"Could not resolve {search_type} "
                             f"{name_to_find} defined in {path_str} "
                             f"as its defined in multiple places with none "
                             f"of them having a hierarchical preference",
                  issue_str=f"{search_type} {name_to_find} "
                            f"could not be resolved")

        return False

    def assign_tab(self):
        # If the tab_by is a string directly look for it otherwise its a level
        # in the path
        tab_by = self.settings["TabBy"]
        tab_str_bool = type(tab_by) == str

        for key, definition in self.definitions.items():
            # If tab_by is a string look for it in the keys of the definition
            if tab_str_bool:
                # If the tab is defined in the definition
                if tab_by in definition:
                    tab_group = definition[tab_by]
                else:
                    tab_group = self.settings["DefaultTab"]
            # If tab is based on path level
            else:
                tab_group = definition["MetaData"]["Path"][tab_by]

            # Set the Tab key to be the assigned tab
            self.definitions[key]["MetaData"]["Tab"] = tab_group

    def assign_group(self):
        # This has to be done after the tabs are assigned to be able to set the
        # correct tab of items that are assigned to a group that are in a custom tab
        group_by = self.settings["GroupBy"]
        group_str_bool = type(group_by) == str

        new_groups = {}

        for key, definition in self.definitions.items():
            # Args can set the group to have a tab
            group_name, group_arg = None, None
            # If the group_by is a string find which definition its pointing to
            if group_str_bool:
                # If the group is defined in the definition
                if group_by in definition:
                    group_name = definition[group_by]
                    # If the group name is not a string assume it's a dict with
                    # one key value pair, otherwise it's not well-defined
                    if type(group_name) != str:
                        try:
                            [(group_name, group_arg)] = group_name.items()
                        except ValueError:
                            self.warn(key=key,
                                      logger_str=f"{definition['MetaData']['PathStr']} "
                                                 f" incorrectly defined Group",
                                      issue_str=f"Incorrect Group definition")
                            group_name = None
            # If the grouping is done based on path level
            else:
                group_name = definition['MetaData']["Path"][group_by]

            # If a group is not defined
            if group_name is None:
                self.definitions[key]["MetaData"]["Parent"] = None
                self.definitions[key]["MetaData"]["ParentArg"] = None
                continue

            # If a group is defined
            # After I got the name of the group, search for it, if found assign to it
            # else create the missing group and assign to it
            element_path = self.find_element(definition["MetaData"]["Path"],
                                             group_name, "Group")
            # If the group exists
            if element_path:
                group = "_".join(element_path)
                # If the definition that it is supposed to be grouped to is not a group
                # if self.definitions[group]["Type"] != "Group":
                #     self.warn(key=key,
                #               logger_str=f"{key} grouped to {group} but it is "
                #                          f"not a Group",
                #               issue_str=f"Cannot group to {group}")
                #     group, group_arg = None, None
                # else:

                # Assign the definition to have the same tab as the group
                self.definitions[key]["MetaData"]["Tab"] = self.definitions[group]["MetaData"]["Tab"]
            # If the group does not exist in the definitions dict make one
            elif element_path is None:
                group = f'{str(self.definitions[key]["MetaData"]["Tab"])}_{group_name}'
                # Check if the group was just created in new_groups
                if group in new_groups:
                    self.definitions[key]["Tab"] = new_groups[group]["MetaData"]["Tab"]
                    new_groups[group]["MetaData"]["Users"] += 1
                # Else create a new group
                else:
                    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                    # This will set the tab of the group to be the tab of the first
                    # definition that is assigned to a non-defined group
                    new_group = {"Type": "Group",
                                 "MetaData": {
                                     "Tab": definition["MetaData"]["Tab"],
                                     "Name": group_name,
                                     "Path": [self.definitions[key]["MetaData"]["Tab"], group_name],
                                     "Parent": None,
                                     "ParentArg": None,
                                     "PathStr": group,
                                 "Users": 1}}
                    new_groups[group] = new_group
            # Else this means that the group could not be resolved
            else:
                group = None

            # Assign the correct group and group_arg
            self.definitions[key]["MetaData"]["Parent"] = group
            self.definitions[key]["MetaData"]["ParentArg"] = group_arg

        self.definitions = self.definitions | new_groups

    # TODO If I want SubSetting keyword to be easily changed do it here
    def assign_sub_setting(self):
        # This should be called after group as it should have priority
        # (can overwrite a group parent)
        to_remove = []
        for key, definition in self.definitions.items():
            sub_setting_arg = None
            if "SubSetting" in definition:
                sub_setting = definition["SubSetting"]
                # If it is not a string then assume its a dict with 1 key value pair
                if type(sub_setting) != str:
                    try:
                        [(sub_setting, sub_setting_arg)] = sub_setting.items()
                    except ValueError:
                        self.warn(key=key,
                                  logger_str=f"{definition['MetaData']['PathStr']} "
                                             f" incorrectly defined SubSetting",
                                  issue_str=f"Incorrect SubSetting definition")
            # if sub setting is not defined
            else:
                continue

            element_path = self.find_element(definition["MetaData"]["Path"],
                                             sub_setting, "SubSetting")
            # If a sub setting with the right name was found
            if element_path:
                parent = definition["MetaData"].get("Parent")

                # If the sub setting is overwriting a group, remove the group
                # if it was newly generated and has no users
                if parent and "Users" in self.definitions[parent]["MetaData"]:
                    self.definitions[parent]["MetaData"]["Users"] -= 1
                    if self.definitions[parent]["MetaData"]["Users"] == 0:
                        to_remove.append(parent)

                # Assign stuff
                path_str = "_".join(element_path)
                self.definitions[key]["MetaData"]["Tab"] = self.definitions[path_str]["MetaData"]["Tab"]
                self.definitions[key]["MetaData"]["Parent"] = path_str
                self.definitions[key]["MetaData"]["ParentArg"] = sub_setting_arg

        for group in to_remove:
            del self.definitions[group]

    def warn(self, key, logger_str, issue_str):
        self.logger.warning(logger_str)

        if "Issues" not in self.definitions[key]["MetaData"]:
            self.definitions[key]["MetaData"]["Issues"] = []
        self.definitions[key]["MetaData"]["Issues"].append(issue_str)


if __name__ == "__main__":
    import logging
    import sys

    root = logging.getLogger()
    root.setLevel(logging.DEBUG)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    root.addHandler(handler)

    x = {"reference1_datastream1_setting1": {"Type": "Group", "Tab": "hello",
                                             "MetaData": {"Path": ["reference1", "datastream1", "setting1"],
                                                          "PathStr": "reference1_datastream1_setting1",
                                                          "Name": "setting1"}},
         "reference1_datastream1_setting2": {"Type": "str", "Group": "setting1",
                                             "MetaData": {"Path": ["reference1", "datastream1", "setting2"],
                                                          "PathStr": "reference1_datastream1_setting2",
                                                          "Name": "setting2"}},
         "reference1_datastream2_setting3": {"Type": "list", "Tab": "shit",
                                             "MetaData": {"Path": ["reference1", "datastream2", "setting3"],
                                                          "PathStr": "reference1_datastream2_setting3",
                                                          "Name": "setting3"}},
         "reference1_datastream2_setting4": {"Type": "int",
                                             "MetaData": {"Path": ["reference1", "datastream2", "setting4"],
                                                          "PathStr": "reference1_datastream2_setting4",
                                                          "Name": "setting4"}},
         "reference2_datastream1_setting1": {"Type": "str", "Tab": "shit", "Group": {"hello": 1, "shit": 2},
                                             "MetaData": {"Path": ["reference2", "datastream1", "setting1"],
                                                          "PathStr": "reference1_datastream1_setting1",
                                                          "Name": "setting1"}},
         "reference2_datastream1_setting2": {"Type": "list", "Group": "hello", "SubSetting": "setting4",
                                             "MetaData": {"Path": ["reference2", "datastream1", "setting2"],
                                                          "PathStr": "reference2_datastream1_setting2",
                                                          "Name": "setting2"}}}

    # [print(key, value) for key, value in flatten_dict(x, 2).items()]
    f = ClusterDefinitions(x,
                  {"TabBy": "Tab",
                   "GroupBy": "Group",
                   "DefaultTab": "default"},
                  root)

    [print(key, value["MetaData"]) for key, value in f.definitions.items()]
