from PySide6.QtWidgets import QStackedWidget, QSizePolicy
from ...Tools import create_widget_boxlayout


class StackedFrame:

    def __init__(self, args, value_callback, state_callback, parent_frame):
        self.args = {arg: {"count": 0} for arg in args}

        self.frame = QStackedWidget()
        for idx, arg in enumerate(self.args.keys()):
            w, layout = create_widget_boxlayout()
            self.args[arg]["widget"] = w
            self.args[arg]["idx"] = idx
            self.frame.addWidget(w)

        self.frame.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)

    def add_frame(self, frame, arg):
        if arg in self.args:
            self.args[arg]["widget"].layout().addWidget(frame.widget,
                                                        self.args[arg]["count"])
            self.args[arg]["count"] += 1
            self.set_size()
        else:
            print(f"{arg} not defined for choice")
            # TODO add logging

    def set_value(self, value):
        if value in self.args:
            idx = self.args[value]["idx"]
            self.frame.setCurrentIndex(idx)
            self.set_size()

    def set_size(self):
        h = self.frame.currentWidget().sizeHint().height()
        self.frame.setFixedHeight(h)

    def get_widget(self):
        return self.frame

    def get_value(self):
        return None
