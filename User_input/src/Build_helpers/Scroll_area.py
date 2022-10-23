from PySide6.QtWidgets import QScrollArea
from ..Tools import QHLine, create_widget_boxlayout


class Scroll(QScrollArea):

    def __init__(self,
                 build_settings):

        super(Scroll, self).__init__()

        self.idx = 0
        self.build_settings = build_settings

        self.widget, self.layout = create_widget_boxlayout(layout="Vertical",
                                                           padding=[0, 10, 0, 0])
        self.setWidget(self.widget)
        self.setWidgetResizable(True)

        self.frames = []

    def insert_frame(self, frame):
        widgets = {}
        # If there is already a frame in it, and it should have a separator
        if self.idx and self.build_settings["AddSeparator"]:
            line = QHLine()
            self.layout.addWidget(line)
            widgets["line"] = line
        # Add the frame widget
        widgets["frame"] = frame
        self.layout.addWidget(frame.widget)
        self.idx += 1

        self.frames.append(widgets)

    def insert_stretch(self):
        self.layout.addStretch()

    def remove_empty_groups(self):
        to_delete = []
        for idx, dicts in enumerate(self.frames):
            if dicts["frame"].meta_data["Type"] == "Group":
                if not dicts["frame"].body.body.layout.count():
                    to_delete.append(idx)

        for idx in to_delete:
            self.frames[idx]["frame"].widget.setParent(None)
            if "line" in self.frames[idx]:
                self.frames[idx]["line"].setParent(None)



