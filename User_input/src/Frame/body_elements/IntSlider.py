from PySide6.QtWidgets import QSlider
from PySide6.QtCore import Qt


class IntSlider:

    def __init__(self, args, value_callback, state_callback, parent_frame):
        self.callback = value_callback
        self.widget = QSlider(Qt.Horizontal)
        self.widget.valueChanged.connect(self.call)

    def call(self):
        value = self.widget.value()
        self.callback(value)

    def get_value(self):
        return self.widget.value()

    def get_widget(self):
        return self.widget

    def set_value(self, value):
        self.widget.blockSignals(True)
        self.widget.setValue(value)
        self.widget.blockSignals(False)

