from ...Templates.Input_elements.QDoubleSlider import DoubleSlider


class FloatSlider:

    def __init__(self, args, value_callback, state_callback, parent_frame):
        self.callback = value_callback
        self.widget = DoubleSlider()
        self.widget.setRange(0, 100)
        self.widget.value_changed.connect(self.call)

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
