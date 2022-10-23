from PySide6.QtWidgets import QMenu
from PySide6.QtCore import Qt
from ..Tools import create_widget_boxlayout
from .Header import Header
from .Description import Description
from .Body_wrapper import BodyWrapper


# Interface requirements
# FrameContainer
#   - get_value() -> returns single (value) object
#   - set_value(value) sets the value of the whole Frame
#   - get_state() -> returns state dictionary
#   - set_state(dict) sets the state dictionary of the Frame
#   - add_frame(frame, arg) -> bool adds the frame to the body of the Frame
#   - update_warning() updates the warnings for the frame
#   - Assumes Frame.meta_data has keys
#       Path, Tab, Parent, ParentArg


class Frame:

    def __init__(self,
                 frame_builder,
                 template: dict,
                 callback,
                 logger):

        self.frame_builder = frame_builder
        self.template = template
        self.callback = callback
        self.logger = logger
        self.meta_data = template["MetaData"]

        self.issues = {"Build": self.meta_data["Issues"]}

        # create a vertical box layout
        self.widget, self.layout = create_widget_boxlayout(
            "Vertical", template["Settings"]["Padding"])

        # self.widget.setStyleSheet("border: 1px solid green")

        self.header, self.description, self.body = None, None, None

        self.expand_state = False
        self.locked_state = False
        self.body_state = None

        self.build_header()
        self.build_description()
        self.build_body()

        self.value = self.collect_value()

        self.state_setters = {
            "ExpandState": self.set_expand_state,
            "LockedState": self.set_locked_state,
            "BodyState": self.set_body_state,
        }

        self.widget.mousePressEvent = self.mouse_click

    # ------------------------ Required Interface ------------------------------
    def get_value(self) -> object:
        return self.collect_value()

    def set_value(self, value, origin: str = None) -> None:
        self.value = value
        if origin != "Body":
            self.set_body_value(value)
        if origin != "Header":
            self.set_header_value(value)

    def get_state(self) -> dict:
        state = {
            "ExpandState": self.expand_state,
            "LockedState": self.locked_state,
            "BodyState": self.body_state
        }
        return state

    def set_state(self, state: dict) -> dict:
        for state_key, state in state.items():
            if state_key in self.state_setters and state is not None:
                self.state_setters[state_key](state)
            else:
                self.logger.warning(f"{self.meta_data['PathStr']} does not have"
                                    f"state {state_key} to set.")

    def add_frame(self, frame, arg=None) -> bool:
        try:
            self.body.add_frame(frame, arg)
            return True
        except AttributeError:
            return False

    def update_warnings(self) -> None:
        self.description.set_hover_tooltip_text()

    def update_layout(self) -> None:
        self.header.match_heights()
    # --------------------------------------------------------------------------

    # -------------------------- State setters ---------------------------------
    def set_expand_state(self, state):
        self.expand_state = state
        if self.header:
            self.header.set_expand_state(state)
        if self.body:
            self.body.set_expand_state(state)

    def set_locked_state(self, state):
        self.locked_state = state
        if self.header:
            self.header.set_locked_state(state)

    def set_body_state(self, state):
        self.body_state = state
        if self.body:
            self.body.set_body_state(state)

    # --------------------------------------------------------------------------

    # -------------------------- Builder functions -----------------------------
    def build_header(self):
        if self.template["Label"] or self.template["InputItem"]:
            self.header = Header(self)
            self.layout.addWidget(self.header.widget)

    def build_description(self):
        self.description = Description(self)
        if self.description.widget:
            self.layout.addWidget(self.description.widget)

    def build_body(self):
        if self.template["Body"]:
            self.body = BodyWrapper(self)
            self.set_expand_state(self.template["Body"]["Expanded"])
            self.layout.addWidget(self.body.widget)

    # --------------------------------------------------------------------------

    # --------------------------- Helper functions -----------------------------
    def set_header_value(self, value):
        if self.header:
            self.header.set_value(value)

    def set_body_value(self, value):
        if self.body:
            self.body.set_value(value)

            if self.template["Body"]["ExpandOnValue"] \
                    and not self.template["Body"]["AlwaysExpanded"]:
                self.set_expand_state(value)

    def set_label_tooltip(self, text):
        if self.header:
            self.header.set_label_tooltip(text)

    def set_label_warning(self, state):
        if self.header:
            self.header.set_warning_state(state)

    def collect_value(self):
        h_value, b_value = None, None
        if self.header:
            h_value = self.header.get_value()
        if self.body:
            b_value = self.body.get_value()

        if h_value is None:
            if b_value is not None:
                return b_value
            else:
                return None
        else:
            if b_value is None:
                return h_value
            else:
                if h_value == b_value:
                    return h_value
                else:
                    self.logger.warning(f"{self.meta_data['PathStr']} has "
                                        f"mismatch between header and body "
                                        f"value, falling back to header value")
                    self.issues["Value Retrieval"] = ["Header and Body "
                                                      "have different values"]
                    self.set_label_warning(True)
                    return h_value

    # --------------------------------------------------------------------------

    # ------------------------------- Callback ---------------------------------
    def value_callback(self, value, origin: str):
        self.set_value(value, origin)
        self.callback(self.meta_data["Path"], value)

    # --------------------------------------------------------------------------

    # --------------------------- Right Click Menu -----------------------------
    def mouse_click(self, event):
        if event.button() == Qt.RightButton:
            self.context_menu_event(event)

    def context_menu_event(self, event):
        if not self.template["Settings"]["AllowLock"]:
            return

        context_menu = QMenu(self.widget)
        if self.locked_state:
            lock_state = context_menu.addAction("Un-Lock")
        else:
            lock_state = context_menu.addAction("Lock")
        action = context_menu.exec_(self.widget.mapToGlobal(event.pos()))
        if action == lock_state:
            state = not self.locked_state
            self.set_locked_state(state)
