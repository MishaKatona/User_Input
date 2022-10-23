from PySide6.QtWidgets import QTextEdit, QSizePolicy
from PySide6.QtCore import QSize


class TextEdit(QTextEdit):

    def __init__(self, max_lines=3, *args, **kwargs):
        super(TextEdit, self).__init__(*args, **kwargs)

        self.max_lines = max_lines if max_lines >= 1 else 1

        # Every time text is changed adjust the height of the text box
        self.textChanged.connect(self.do_shit)
        self.focusEvent = self.on_focus

        # Set the empty text box to a height of 1 line
        self.default = self.document().documentLayout().documentSize().height()
        self.setMaximumHeight(self.default + 3)
        self.setMinimumWidth(10)
        self.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Maximum)
        # self.sizePolicy().setHorizontalPolicy(QSizePolicy.Maximum)

    def do_shit(self):
        height = self.get_clamped_height()
        self.setMaximumHeight(height + 3)

    def on_focus(self, event):
        self.setMaximumHeight(self.get_clamped_height() + 3)

    def sizeHint(self):
        return QSize(10, self.default + 3)

    def get_clamped_height(self):
        height = self.document().documentLayout().documentSize().height()

        # default is the height of the first line, subsequent lines are 8 shorter
        max_height = self.default + (self.default - 8) * (self.max_lines - 1)

        return height if height <= max_height else max_height

