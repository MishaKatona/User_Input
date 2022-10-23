from PySide6.QtWidgets import QColorDialog, QPushButton
from PySide6.QtGui import QColor


class PickColor:

    def __init__(self, args, value_callback, state_callback, parent_frame):
        self.state = (0, 0, 0)
        self.callback = value_callback

        self.frame = QPushButton("Pick color")
        self.frame.clicked.connect(self.pick_color)

    def get_widget(self):
        return self.frame

    def set_value(self, value):
        self.set_state(value)

    def pick_color(self):
        if self.state:
            initial_color = QColor(*self.state)
            color = QColorDialog.getColor(initial=initial_color)
        else:
            color = QColorDialog.getColor()

        if color.isValid():
            self.set_state(color.getRgb()[:3])
            self.callback(color.getRgb()[:3])

    def set_state(self, state):
        self.state = state
        color = QColor(*state)

        if color.lightnessF() < 0.3:
            text_color = "; color: white"
        else:
            text_color = "; color: black"

        self.frame.setStyleSheet(f"background-color: {color.name()}" + text_color)

    def get_value(self):
        return self.state

