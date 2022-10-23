from ..Tools import create_widget_boxlayout
from PySide6.QtWidgets import QSizePolicy

# Required Body Interface
#   - get_widget() -> pyside element (something that I can add in a layout)
#   - set_value(value) sets the value of the body
#   - get_value() -> returns current value
#   - set_state(state) sets state of the body
# Optional
#   - if layout attribute stores the layout then I can hide empty layouts


class BodyWrapper:

    def __init__(self, parent_frame):
        self.parent = parent_frame
        body_tmplt = parent_frame.template["Body"]

        self.widget, self.layout = create_widget_boxlayout(
            layout="Vertical", padding=[body_tmplt["Indent"], 0, 0, 0])
        # self.widget.setStyleSheet("border: 1px solid green")
        self.widget.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum)

        self.body = body_tmplt["Widget"](args=body_tmplt["Args"],
                                         value_callback=self.value_callback,
                                         state_callback=self.state_callback,
                                         parent_frame=self.parent)

        self.layout.addWidget(self.body.get_widget())
        self.is_expanded = False
        # self.set_size()

    def set_size(self):
        h = self.layout.sizeHint().height()
        self.widget.setFixedHeight(h)

    def add_frame(self, frame, args):
        self.body.add_frame(frame, args)
        if self.is_expanded:
            self.set_expand_state(True)

    def set_expand_state(self, state):
        self.is_expanded = state
        elements = True
        if hasattr(self.body, "layout"):
            if not self.body.layout.count():
                elements = False
        if elements:
            self.widget.setVisible(bool(state))
        else:
            self.widget.setVisible(False)

    def value_callback(self, value):
        self.parent.value_callback(value, "Body")

    def set_value(self, value):
        self.body.set_value(value)

    def get_value(self):
        return self.body.get_value()

    def state_callback(self, state):
        self.parent.set_body_state(state)

    def set_body_state(self, state):
        self.body.set_state(state)






