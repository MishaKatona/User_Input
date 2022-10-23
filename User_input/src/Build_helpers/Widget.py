from PySide6.QtWidgets import QTabWidget
from .Scroll_area import Scroll


class Widget:

    def __init__(self,
                 frame_container,
                 build_settings):

        self.frame_container = frame_container
        self.build_settings = build_settings

        self.tabs = self.generate_tabs()
        self.populate_tabs()
        self.widget = self.create_widget()

        self.frame_container.update_layout()

    def generate_tabs(self):
        tab_lst = sorted(self.frame_container.get_tabs())
        tabs = {}

        for tab in tab_lst:
            tabs[tab] = Scroll(self.build_settings)

        return tabs

    def populate_tabs(self):
        for frame, tab, parent in self.frame_container.iterator():
            success = True
            if parent:
                success = self.frame_container.set_frame_parent(parent, frame)
            if not parent or not success:
                self.tabs[tab].insert_frame(frame)

        # Add stretch at the bottom of all tabs
        for tab in self.tabs.values():
            tab.remove_empty_groups()
            tab.insert_stretch()

    def populate_layout(self, layout):
        for frame, tab, parent in self.frame_container.iterator():
            success = True
            if parent:
                success = self.frame_container.set_frame_parent(parent, frame)
            if not parent or not success:
                layout.addWidget(frame.widget)

    def create_widget(self):
        if len(self.tabs) == 1:
            [(key, tab)] = self.tabs.items()
            return tab
        else:
            widget = QTabWidget()
            for tab_name, scroll_are in self.tabs.items():
                widget.addTab(scroll_are, tab_name)
            return widget

    def get_widget(self):
        return self.widget

    def set_values(self, values):
        self.frame_container.set_values(values)

    def get_values(self):
        return self.frame_container.get_values()

    def set_state(self, state):
        self.frame_container.set_state(state)

    def get_state(self):
        return self.frame_container.get_state()

