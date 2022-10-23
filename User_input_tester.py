# This Python file uses the following encoding: utf-8
import os
import json

from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout
from PySide6.QtCore import QFile
from PySide6.QtUiTools import QUiLoader

from User_input.User_input_widget import UIWidget
from User_input.src.Templates.Default_template import default
from User_input.src.Templates.Type_templates import templates

from User_input.Testing.Default_template_definitions import default_input_definition
from User_input.Testing.Definition_test import test_definition

import logging
import sys

root = logging.getLogger("logger")
root.setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
root.addHandler(handler)

# test_definition = {"Key": {"Type": "int"}}


class main(QMainWindow):
    def __init__(self):
        super(main, self).__init__()
        self.load_ui()
        self.ui = self.centralWidget()
        self.ui.button_compile.clicked.connect(self.get_content)
        self.ui.button_get_input.clicked.connect(self.get_values)
        self.ui.button_set_input.clicked.connect(self.set_value)

        self.default = None
        self.w = None
        self.build_default_widget()
        self.ui.text_templates.setPlainText(json.dumps(templates, indent=4))
        self.ui.text_user_defined.setPlainText(json.dumps(test_definition, indent=4))
        self.widget = None
        self.get_content()

    def load_ui(self):
        loader = QUiLoader()
        path = os.path.join(os.path.dirname(__file__), "User_input/Testing/form.ui")
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        loader.load(ui_file, self)
        ui_file.close()

    def build_default_widget(self):
        templates_t = templates

        build_settings = {"Clustering": {"TabBy": "Tab", "GroupBy": 1,
                                         "DefaultTab": "default"},
                          "AddSeparator": True}

        build_default = {"Clustering": {"TabBy": "Tab", "GroupBy": "Group",
                                        "DefaultTab": "default"},
                         "AddSeparator": True}

        default_extended = default.copy()
        values = {"DefaultTemplate": default_extended,
                  "BuildSettings": {"BuildSettings": build_default}}

        self.default = UIWidget(definitions=default_input_definition,
                                definition_depth=2,
                                callback=self.default_callback,
                                logger_name="Default_Template",
                                build_settings=build_settings,
                                values=values)

        layout = QVBoxLayout()
        layout.addWidget(self.default)
        self.ui.widget_default.setLayout(layout)

    def set_value(self):
        if self.w:
            self.w.set_values({"Data Stream 1": {"hello": 1000,
                                                 "hello2": 5000,
                                                 "hello3": "We Do",
                                                 "hello8": 42}})
            self.w.set_state({"Data Stream 1": {"Guess": {"ExpandState": True},
                                                "hello": {"LockedState": True},
                                                "hello8": {"LockedState": False,
                                                           "ExpandState": True}}})

    def build_settings(self, user_input, templates_t):
        template = self.default.get_values()
        default_t = template["DefaultTemplate"]
        build_settings = template["BuildSettings"]["BuildSettings"]

        default_t["Description"]["Text"] = False
        default_t["Settings"]["Padding"] = [5, 0, 5, 0]
        default_t["Body"]["Args"] = {}

        templates_t["bool"]["Body"] = {"ExpandOnValue": True}

        self.w = UIWidget(definitions=user_input,
                          definition_depth=2,
                          callback=self.custom,
                          logger_name="Test_Inputs",
                          build_settings=build_settings,
                          default_template=default_t)

        QWidget().setLayout(self.ui.widget_user_defined.layout())
        layout = QVBoxLayout()
        layout.addWidget(self.w)
        self.ui.widget_user_defined.setLayout(layout)

    def get_values(self):
        if self.w:
            [print(key, value) for key, value in self.w.get_values().items()]
            print()
            [print(key, value) for key, value in self.w.get_state().items()]

    def custom(self, path, name):
        print(path, name)

    def default_callback(self, path, name):
        pass

    def get_content(self):
        values = self.ui.text_user_defined.toPlainText()
        user_input = json.loads(values)
        values = self.ui.text_templates.toPlainText()
        templates_t = json.loads(values)
        self.build_settings(user_input, templates_t)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    widget = main()
    widget.centralWidget().show()
    sys.exit(app.exec_())
