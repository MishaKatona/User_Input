from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
import sys

from .User_input_widget import UIWidget


class Main(QMainWindow):

    def __init__(self,
                 definitions: dict,
                 definition_depth: int,
                 callback=None,
                 build_settings: dict = None,
                 values: dict = None,
                 state: dict = None):
        super(Main, self).__init__()
        self.setCentralWidget(QWidget())
        self.ui = self.centralWidget()
        self.ui.setLayout(QVBoxLayout())

        self.widget = UIWidget(definitions,
                               definition_depth,
                               callback,
                               build_settings,
                               values,
                               state)

        self.ui.layout().addWidget(self.widget)

    def get_values(self):
        return self.widget.get_values()


def build_window(definitions: dict,
                 definition_depth: int,
                 callback=None,
                 build_settings: dict = None,
                 values: dict = None,
                 state: dict = None):
    if not QApplication.instance():
        app = QApplication(sys.argv)
    else:
        app = QApplication.instance()
    app.setQuitOnLastWindowClosed(True)
    widget = Main(definitions=definitions,
                  definition_depth=definition_depth,
                  callback=callback,
                  build_settings=build_settings,
                  values=values,
                  state=state)
    widget.resize(400, 600)
    widget.show()
    wait = app.exec()
    return widget.get_values()


if __name__ == "__main__":
    shit = build_window({"Hello": {"Type": "int"},
                              "Other": {"Type": "float"}}, 0)
    print(shit)
