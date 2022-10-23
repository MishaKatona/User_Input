

class InputItem:

    def __init__(self,
                 template,
                 callback):

        self.template = template
        self.callback = callback
        self._args = {}

        self.input_item = self.__create_item()
        if "Change" in self.template:
            # set callback to pass value back to the frame
            getattr(self.input_item, self.template["Change"]).connect(self.on_change)
        else:
            self.input_item.focusOutEvent = self.on_change

    def __create_item(self):
        """Create the PySide input widget, and set the supplied settings"""
        # If the input widget is expecting some input on initialisation
        if "Input" in self.template:
            item = self.template["Widget"](**self.template["Input"])
        else:
            item = self.template["Widget"]()

        # If the input item is choice, populate the QComboBox
        if "cbox_items" in self.template:
            for option in self.template["cbox_items"]:
                val, display = option, option
                if type(option) == list:
                    val, display = option[0], option[1]
                self._args[display] = val
                item.addItem(str(display))

        # If additional settings can be applied to the input item
        if "Settings" in self.template:
            for key, value in self.template["Settings"].items():
                try:
                    if type(value["Default"]) == dict:
                        getattr(item, value["PysideCall"])(**value["Default"])
                    elif type(value["Default"]) == list:
                        getattr(item, value["PysideCall"])(*value["Default"])
                    else:
                        getattr(item, value["PysideCall"])(value["Default"])
                except Exception as e:
                    x = 1
                    # TODO add logging call here if the setting cannot be done

        return item

    def set_value(self, value):
        """Sets the value of the PySide input widget"""
        if value is not None:
            # if the element is a choice type it needs special handling
            if "cbox_items" in self.template:
                # set value of choice
                key = [key for key, val in self._args.items() if val == value][0]
                value = self.input_item.findText(key)

            # If values needs to be formatted to set it
            if "SetFormatter" in self.template:
                value, issue = self.template["SetFormatter"](value)

            # get the method call to set the value
            self.input_item.blockSignals(True)
            getattr(self.input_item, self.template["Set"])(value)
            self.input_item.blockSignals(False)

    def get_value(self):
        """Gets the value of item"""
        value = getattr(self.input_item, self.template["Get"])()
        if self._args:
            return self._args[value]
        # this can be used in the future for text field inputs
        if "Format" in self.template:
            value, str_value = self.template["Format"](value)
            self.set_value(str_value)
        return value

    def on_change(self, var=None):
        """Injects the value into the callback function"""
        self.callback(self.get_value())
