from PySide6.QtWidgets import QSlider
from PySide6.QtCore import Signal, Qt


class DoubleSlider(QSlider):

    # create our our signal that we can connect to if necessary
    value_changed = Signal(float)

    def __init__(self, Decimals=3, *args, **kwargs):
        super(DoubleSlider, self).__init__(*args, **kwargs, orientation=Qt.Horizontal)
        self._multi = 10 ** Decimals

        self.valueChanged.connect(self.emitDoubleValueChanged)

    def emitDoubleValueChanged(self):
        value = float(super(DoubleSlider, self).value())/self._multi
        self.value_changed.emit(value)

    def value(self):
        return float(super(DoubleSlider, self).value()) / self._multi

    def setMinimum(self, value):
        return super(DoubleSlider, self).setMinimum(int(value * self._multi))

    def setMaximum(self, value):
        return super(DoubleSlider, self).setMaximum(int(value * self._multi))

    def setRange(self, min_val, max_val):
        return super(DoubleSlider, self).setRange(int(min_val * self._multi),
                                                  int(max_val * self._multi))

    def setSingleStep(self, value):
        return super(DoubleSlider, self).setSingleStep(int(value * self._multi))

    def singleStep(self):
        return float(super(DoubleSlider, self).singleStep()) / self._multi

    def setValue(self, value):
        super(DoubleSlider, self).setValue(int(value * self._multi))
