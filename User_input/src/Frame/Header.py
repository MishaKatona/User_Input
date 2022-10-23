from PySide6.QtCore import Qt, QSize
from PySide6.QtWidgets import QToolButton
from ..Tools import create_widget_boxlayout
from .Label import IconLabel
from .Input_item import InputItem

alignments = {"Left": Qt.AlignLeft, "Center": Qt.AlignCenter,
              "Right": Qt.AlignRight, "Fill": False,
              "Top": Qt.AlignTop}


class Header:

    def __init__(self,
                 parent_frame):

        self.parent = parent_frame
        self.template = parent_frame.template

        self.widget, self.layout = create_widget_boxlayout("Grid")

        self.label, self.input_item, self.expand_button = None, None, None

        self.build_label()
        self.build_input_item()
        self.build_expand_button()

    # ------------------------ Required Interface ------------------------------
    def set_value(self, value):
        if self.input_item:
            self.input_item.set_value(value)

    def set_expand_state(self, state):
        if self.expand_button:
            if state:
                self.expand_button.setArrowType(Qt.DownArrow)
            else:
                self.expand_button.setArrowType(Qt.LeftArrow)

            if self.input_item and self.template["InputItem"]["HideOnExpand"]:
                self.input_item.input_item.setVisible(not state)

    def set_locked_state(self, state):
        if self.label:
            self.label.set_locked_state(state)

    def set_warning_state(self, state):
        if self.label:
            self.label.set_warning_state(state)

    def set_label_tooltip(self, text):
        if self.label:
            self.label.set_tooltip(text)

    def get_value(self):
        if self.input_item:
            return self.input_item.get_value()
        return None
    # --------------------------------------------------------------------------

    # -------------------------- Builder functions -----------------------------
    def build_label(self):
        if self.template["Label"]:
            self.label = IconLabel(template=self.template["Label"])

            alignment = alignments[self.template["Label"]["Alignment"]]
            self.layout.addWidget(self.label, 0, 0,
                                  alignment=alignment | alignments["Top"])

    def build_input_item(self):
        if self.template["InputItem"]:
            # TODO use self.value_callback
            self.input_item = InputItem(template=self.template["InputElement"],
                                        callback=self.value_callback)

            item = self.input_item.input_item
            input_template = self.template["InputItem"]

            align = {}
            if alignments[input_template["Alignment"]]:
                align["alignment"] = alignments[input_template["Alignment"]]

            location = []
            if input_template["Location"] == "Right":
                location = [0, 1]
            elif input_template["Location"] == "Below":
                location = [1, 0, 1, -1]

            self.layout.addWidget(item, *location, **align)

    def build_expand_button(self):
        if self.template["ExpandButton"]:
            size = self.template["ExpandButton"]["Size"]
            self.expand_button = QToolButton()
            self.expand_button.setArrowType(Qt.DownArrow)
            self.expand_button.setIconSize(QSize(size, 20))
            if not self.template["ExpandButton"]["Border"]:
                self.expand_button.setStyleSheet("border:None")
            self.expand_button.clicked.connect(self.change_expand_state)
            self.layout.addWidget(self.expand_button, 0, 2,
                                  alignment=alignments["Top"])
    # --------------------------------------------------------------------------

    # ------------------------------ Callbacks ---------------------------------
    def value_callback(self, value):
        """Inject that this is a header callback in the callback"""
        self.parent.value_callback(value, origin="Header")

    def change_expand_state(self):
        state = not self.parent.expand_state
        self.parent.set_expand_state(state)
    # -------------------------------------------------------------------------

    # ------------------------------- Helpers ---------------------------------
    def match_heights(self):
        if self.input_item:
            height = self.input_item.input_item.sizeHint().height()

            if self.label:
                if self.label.height() < height:
                    self.label.setFixedHeight(height)
            if self.expand_button:
                size = self.template["ExpandButton"]["Size"]
                self.expand_button.setIconSize(QSize(size, height))


