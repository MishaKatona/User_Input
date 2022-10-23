from .Widget_builder import WidgetBuilder
import logging


class UserInput:
    """
    High level interface class for the input widget

    Methods:
        - get_input_widget: returns the Pyside widget
        - set_values(dict): sets the values of the frames in the widget
        - get_values: returns the values of all frames in the widget
        - set_state(dict): sets the state of the frames in the widget
        - get_state: returns the state of all frames in the widget
    """

    def __init__(self,
                 default_template: dict,
                 template_list: list[dict],
                 input_definitions: dict,
                 definitions_depth: int,
                 build_settings: dict,
                 input_element_templates: dict[str, dict],
                 body_dict_list: list[dict],
                 logger_name: str,
                 callback,
                 values: dict = None,
                 state: dict = None):
        """
        Inputs:
            - default_template: contains default values for all possible fields
            - template_list: list of dictionaries that (re)define templates
                             with priority going from low->high
            - input_definitions: (nested) dictionary containing the definition
                                 of each input element (frame)
            - definitions_depth: indicates the number of groups/nesting in the
                                 input_definition before the definitions
                                 (all definitions must be on this level)
            - input_element_templates:
            - body_dict_list:
            - values: values to set the frames defined by input_definitions
                      (must have same shape and keys as input_definitions)
            - state: state of each frame defined by the input definitions
                     (must have same shape and keys as input_definitions)
                     (all information that is unique to the frames)
        """

        self.input_definitions = input_definitions
        self.definitions_depth = definitions_depth
        self.callback = callback

        if logger_name is None:
            logger_name = "User_Input_Logger"
        self.logger = logging.getLogger(logger_name)

        self.widget_builder = WidgetBuilder(default_template=default_template,
                                            template_lst=template_list,
                                            input_element_template=input_element_templates,
                                            body_dict_list=body_dict_list,
                                            build_settings=build_settings,
                                            logger=self.logger)

        self.input_widget = self.__build_input_widget()

        if values:
            self.set_values(values)

        if state:
            self.set_state(state)

    def __build_input_widget(self):
        """
        Builds the input_widget that contains all the input frames
        Inputs:
            - values: values to set the frames defined by input_definitions
                      (must have same shape and keys as input_definitions)
            - state: state of each frame defined by the input definitions
                     (must have same shape and keys as input_definitions)
                     (all information that is unique to the frames, i.e not values)
        """

        widget = self.widget_builder.build_widget(input_definitions=self.input_definitions,
                                                  definitions_depth=self.definitions_depth,
                                                  callback=self.UI_callback)

        return widget

    def get_input_widget(self):
        """Returns the generated input widget"""
        return self.input_widget.get_widget()

    def UI_callback(self, path, value):
        """Callback wrapper"""
        if self.callback is not None:
            self.callback(path, value)

    def set_state(self, state: dict):
        """
        Sets the state of the input widget frames
        Inputs:
            - state: state of each frame defined by the input definitions
                     (must have same shape and keys as input_definitions)
                     (all information that is unique to the frames, i.e not values)
        """
        self.input_widget.set_state(state)

    def get_state(self):
        """Returns the state of all the frames in the input widget"""
        return self.input_widget.get_state()

    def set_values(self, values: dict):
        """
        Sets the values of the input widget frames
        Inputs:
            - values: values to set the frames defined by input_definitions
                      (must have same shape and keys as input_definitions)
        """
        self.input_widget.set_values(values)

    def get_values(self):
        """Returns the values of all the frames in the input widget"""
        return self.input_widget.get_values()
