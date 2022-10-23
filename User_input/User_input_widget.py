from PySide6.QtWidgets import QWidget, QVBoxLayout

from .src.User_input import UserInput
from .src.Tools import dump_dict_resource, load_dict_like_resource

from .src.Templates.Type_templates import templates
from .src.Templates.Default_template import default
from .src.Templates.Input_element_templates import input_elements
from .src.Frame.body_elements.Body_elements import body_widget


class UIWidget(QWidget):

    def __init__(self,
                 definitions: dict,
                 definition_depth: int,
                 callback=None,
                 logger_name: str = None,
                 build_settings: dict = None,
                 type_templates: list[dict] = None,
                 default_template: dict = None,
                 values: dict = None,
                 state: dict = None):

        super(UIWidget, self).__init__()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.callback = callback
        self.definition_depth = definition_depth
        self.logger_name = logger_name

        self.definitions, _ = load_dict_like_resource(resource=definitions)


        self.build_settings, _ = load_dict_like_resource(
            resource=build_settings,
            default={"Clustering": {"TabBy": "Tab",
                                    "GroupBy": "Group",
                                    "DefaultTab": "default"},
                     "AddSeparator": True})

        self.default_template, _ = load_dict_like_resource(
            resource=default_template,
            default=default
        )

        self.type_templates = [templates]
        if [type_templates] == list:
            for template in type_templates:
                new, _ = load_dict_like_resource(
                    resource=template,
                )
                if new is not None:
                    # Add the new template definitions to the default
                    self.type_templates += [new]

        self.values = values if values else {}
        self.state = state if state else {}

        self.user_input = self.build_user_input()
        self.widget = self.user_input.get_input_widget()

        self.layout.addWidget(self.widget)

    def build_user_input(self):
        user_input = UserInput(default_template=self.default_template,
                               template_list=self.type_templates,
                               input_definitions=self.definitions,
                               definitions_depth=self.definition_depth,
                               build_settings=self.build_settings,
                               input_element_templates=input_elements,
                               body_dict_list=[body_widget],
                               logger_name=self.logger_name,
                               callback=self.callback,
                               values=self.values,
                               state=self.state)

        return user_input

    def get_values(self):
        return self.user_input.get_values()

    def set_values(self, values):
        self.user_input.set_values(values=values)

    def get_state(self):
        return self.user_input.get_state()

    def set_state(self, state):
        self.user_input.set_state(state=state)

