from PySide6.QtGui import QFont, QPixmap
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QLabel, QHBoxLayout
import os


class IconLabel(QWidget):

    def __init__(self, template: dict):
        super(IconLabel, self).__init__()
        self.template = template
        self.icon_size = self.template["IconSize"]
        self.max_width = self.template["MaxWidth"]

        # self.setStyleSheet("border: 1px solid green")

        self.prefix_state, self.suffix_state = False, False

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        self.prefix_icon = QLabel()
        self.label = self.build_label()
        self.suffix_icon = QLabel()
        self.padding = QLabel()

        self.set_locked_state(False)
        self.set_warning_state(False)
        self.padding.setVisible(False)

        layout.addWidget(self.prefix_icon)
        layout.addWidget(self.label)
        layout.addWidget(self.suffix_icon)
        layout.addWidget(self.padding)

        layout.setSpacing(1)

    def set_icon(self, icon, icon_name):
        if not icon_name:
            icon.setVisible(False)
        else:
            icon.setVisible(True)
            # TODO this has to be changed for the icons
            pixmap = QPixmap(f"{os.path.dirname(__file__)}/{icon_name}.png")
            pixmap = pixmap.scaled(self.icon_size, self.icon_size, Qt.KeepAspectRatio)
            icon.setPixmap(pixmap)
        self.set_label_width()

    def set_label_width(self):
        icon_space = 0
        if self.prefix_state:
            icon_space += self.icon_size + 1
        if self.suffix_state:
            icon_space += self.icon_size + 1

        max_label_width = self.max_width - icon_space
        width = self.label.fontMetrics().boundingRect(self.label.text()).width()

        if width > max_label_width or not self.suffix_state:
            self.label.setFixedWidth(max_label_width)
            self.padding.setVisible(False)
        else:
            self.label.setFixedWidth(width + 5)
            diff = max_label_width - width - 5
            if diff > 2:
                self.padding.setFixedWidth(diff - 1)
                self.padding.setVisible(True)

    def build_label(self):
        label = QLabel(self.template["Text"])
        label.setWordWrap(True)
        label.setFixedWidth(self.template["MaxWidth"])

        # Set font characteristics
        if self.template["Bold"] or self.template["Italic"]:
            font = QFont()
            font.setBold(self.template["Bold"])
            font.setItalic(self.template["Italic"])
            label.setFont(font)

        return label

    def set_tooltip(self, tooltip_str: str):
        self.setToolTip(tooltip_str)

    def set_locked_state(self, state):
        self.prefix_state = state
        icon = "lock" if state else False
        self.set_icon(self.prefix_icon, icon)

    def set_warning_state(self, state):
        self.suffix_state = state
        icon = "warning" if state else False
        self.set_icon(self.suffix_icon, icon)
