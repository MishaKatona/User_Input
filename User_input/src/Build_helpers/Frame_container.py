from ..Tools import flatten, nest

# !!!!!!!!!!!!!!
# ASSUMPTIONS
# frame has "get/set_value", "get/set_state", and "add_frame" method interface


class FrameContainer:
    """Wrapper class that allows for easy interaction between the internal
    flat dict representation and external nested dict representation"""

    def __init__(self,
                 dict_depth: int,
                 logger):

        self.dict_depth = dict_depth
        self.logger = logger
        self.frames = {}
        self.paths = None
        self.tabs = None

    def retrieve_information(self) -> dict:
        """Extracts the path lists from the definitions"""
        paths = {}
        tabs = set()
        for key, frame in self.frames.items():
            paths[key] = frame.meta_data["Path"]
            tabs.add(frame.meta_data["Tab"])
        self.paths = paths
        self.tabs = list(tabs)

    def add_frame(self, key: str, frame):
        """Add frame"""
        self.frames[key] = frame

    def set_frame_parent(self, parent_key, frame):
        """Assigns a frame to its parent frame"""
        if parent_key in self.frames:
            parent_arg = frame.meta_data["ParentArg"]
            success = self.frames[parent_key].add_frame(frame, parent_arg)
            if not success:
                self.logger.warning(f"{frame.meta_data['PathStr']} cannot be "
                                    f"grouped with {parent_key} because it is "
                                    f"not a container type")
                frame.issues["Compile"] = [f"Cannot group to {parent_key}"]
                frame.update_warnings()
            return success
        else:
            raise KeyError(f"{parent_key} does not exist, cannot assign a frame to it")

    def get_tabs(self) -> list:
        """Returns a list of tabs that are in the frames"""
        return self.tabs

    def get_paths(self) -> dict:
        """Returns the paths dict"""
        return self.paths

    def set_values(self, values_dict: dict) -> None:
        values_dict = flatten(values_dict, self.dict_depth)

        for key, value in values_dict.items():
            if key in self.frames:
                self.frames[key].set_value(value)
            else:
                self.logger.warning(f"No frame that matches key {key}, "
                                    f"cannot set value")

    def set_state(self, state_dict: dict[str, dict]) -> None:
        """Set the state dictionary of each frame"""
        state_dict = flatten(state_dict, self.dict_depth)

        for key, state in state_dict.items():
            if key in self.frames:
                self.frames[key].set_state(state)
            else:
                self.logger.warning(f"No frame that matches key {key}, "
                                    f"cannot set state")

    def get_values(self) -> dict:
        value_dict = {}
        for key, frame in self.frames.items():
            value_dict[key] = frame.get_value()

        return nest(value_dict, self.paths)

    def get_state(self) -> dict:
        state_dict = {}
        for key, frame in self.frames.items():
            state_dict[key] = frame.get_state()

        return nest(state_dict, self.paths)

    def iterator(self) -> [object, str, str]:
        """Yields the frame, tab, parent in the container"""
        for key, frame in self.frames.items():
            yield frame, frame.meta_data["Tab"],\
                  frame.meta_data["Parent"]

    def update_layout(self) -> None:
        for frame in self.frames.values():
            frame.update_layout()




