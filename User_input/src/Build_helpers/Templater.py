from ..Tools import merge_templates, update_component, merger_dictionaries
from copy import deepcopy


class Templater:

    def __init__(self,
                 default_template: dict,
                 template_lst: list,
                 input_element_template: dict,
                 body_dict_list: dict,
                 logger):

        self.default = default_template
        self.input_element_templates = input_element_template
        # Merge the body definitions from the list with low -> high priority
        self.body_dict = merger_dictionaries(body_dict_list)
        self.logger = logger

        # Merge the templates from the list with low -> high priority
        self.templates = merge_templates(default=default_template,
                                         template_lst=template_lst,
                                         logger=self.logger)

        self.template, self.metadata, self.user_defined = None, None, None

    def create_new_frame(self,
                         user_defined: dict,
                         settings_overwrite: dict = None):

        self.metadata = user_defined["MetaData"]
        if "Issues" not in self.metadata:
            self.metadata["Issues"] = []
        self.user_defined = user_defined

        self.template = self.get_template()
        self.template["MetaData"] = self.metadata

        self.update_label()
        self.update_input_item()
        self.update_input_element()
        self.update_description()
        self.update_body()
        self.update_expand_button()
        # self.update_settings(settings_overwrite)

        return self.template

    def update_label(self):
        self.update_component("Label")

        # Check if user defined custom text for label, otherwise use Name
        if self.template["Label"]:
            if "Text" in self.user_defined and self.user_defined["Text"]:
                self.template["Label"]["Text"] = self.user_defined["Text"]
            else:
                self.template["Label"]["Text"] = self.metadata["Name"]

    def update_input_item(self):
        self.update_component("InputItem")

        if self.template["InputItem"]:
            # Check if the type specified in the input item is a valid input element
            in_type = self.template["InputItem"]["Type"]
            if in_type not in self.input_element_templates:
                self.template["InputItem"] = False

                self.logger.warning(f"{self.metadata['PathStr']} did not "
                                    f"contain a valid type: '{in_type}' "
                                    f"for the InputItem")
                self.metadata["Issues"].append("Incorrect type for InputItem")

    def update_input_element(self):
        self.template["InputElement"] = False

        if self.template["InputItem"]:
            element = self.input_element_templates[self.template["InputItem"]["Type"]]
            template = deepcopy(element)

            # TODO I assume that input element template input will have the
            #  same shape as settings !!!!!!!!!!!!!!!!!!!!!!!!!!!!!

            # Take the inputs and settings defined in InputItem
            template = self.extract_input_element_args(template, "Inputs")
            template = self.extract_input_element_args(template, "Settings")

            if self.template["InputItem"]["Type"] == "Choice":
                if "Options" in self.user_defined:
                    template["cbox_items"] = self.user_defined["Options"]
                else:
                    self.logger.warning(f"{self.metadata['PathStr']} is Type "
                                        f"Choice, but its definition does not "
                                        f"contain the keyword Options (list).")
                    self.metadata["Issues"].append("No Options defined for "
                                                   "Choice")

            self.template["InputElement"] = template

    def update_description(self):
        self.update_component("Description")

        # If there is no text don't return description
        if not self.template["Description"]["Text"]:
            self.template["Description"] = False

    def update_body(self):
        self.update_component("Body")

        if self.template["Body"] and self.template["Body"]["Widget"] == "None":
            self.template["Body"] = False
            return

        # If input item type is choice then pass the options to the body
        if self.template["InputItem"] and \
                self.template["InputItem"]["Type"] == "Choice":
            if self.template["Body"]:
                self.template["Body"]["Args"] = self.user_defined["Options"]

        # if it is always expanded then it should currently be expanded
        if self.template["Body"] and self.template["Body"]["AlwaysExpanded"]:
            self.template["Body"]["Expanded"] = True

        if self.template["Body"]:
            widget = self.template["Body"].get("Widget")
            if widget in self.body_dict:
                self.template["Body"]["Widget"] = self.body_dict[widget]
            else:
                self.logger.warning(f"Body widget with name {widget} not "
                                    f"defined, please change name or create it")
                self.metadata["Issues"].append("Incorrect name for Body widget")
                self.template["Body"] = False

    def update_expand_button(self):
        body = self.template["Body"]
        # Show if there is a body and not always expanded or
        # the value does not control expansion
        if body and not body["AlwaysExpanded"] and not body["ExpandOnValue"]:
            self.update_component("ExpandButton")
        # Else there is no need for the button
        else:
            self.template["ExpandButton"] = False

    def update_settings(self, settings_overwrite):
        self.update_component("Settings")

        if self.settings_overwrite:
            self.template["Settings"].update(settings_overwrite)

    def get_template(self):
        """Returns the template to use for a given user defined frame"""

        name = self.user_defined.get("Template", None)
        if name is not None:
            # If the name of the template is one of the templates
            if name in self.templates:
                self.metadata["Type"] = name
                return deepcopy(self.templates[name])
            # If the name of the template was not found in the templates
            else:
                self.logger.warning(f"{self.metadata['PathStr']} set Template "
                                    f"as {name}, which is not defined. "
                                    f"Attempting to use Type...")

        # If template was incorrectly defined or not at all try using type
        name = self.user_defined.get("Type", None)
        if name is not None and name in self.templates:
            self.metadata["Type"] = name
            return deepcopy(self.templates[name])
        # If the type is not defined or did not match a template
        else:
            self.logger.warning(f"{self.metadata['PathStr']} did not have a "
                                f"valid template defined, falling back to "
                                f"default. Please correctly define "
                                f"'Template' or 'Type'.")
            self.metadata["Issues"].append("Using default template")
            self.metadata["Type"] = "Default"
            return deepcopy(self.default)

    def update_component(self, component):
        # If the component is not defined by the user
        if component not in self.user_defined:
            return

        # else update the component in the template
        self.template[component] = update_component(component=component,
                                                    target=self.template[component],
                                                    updater=self.user_defined[component],
                                                    default=self.default[component])

    def extract_input_element_args(self, element_template, arg_type):
        """Gets the settings and inputs for the input element"""
        if arg_type in element_template:
            for key in element_template[arg_type].keys():
                if key in self.template["InputItem"].keys():
                    element_template[arg_type][key]["Default"] \
                        = self.template["InputItem"][key]
                    # remove it form the input item (its in the inputs now)
                    del self.template["InputItem"][key]
        return element_template

