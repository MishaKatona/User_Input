from ...Tools import create_widget_boxlayout
from PySide6.QtWidgets import QPushButton, QLineEdit, QLabel
import copy


# TODO move key input and button to same line (dont use frame)
#  and have the order of the two be input field then button
class DictBuilder:

    def __init__(self, args, value_callback, state_callback, parent_frame):
        self.parent = parent_frame
        self.builder = parent_frame.frame_builder
        self.args = args
        self.value_callback = value_callback
        self.saved = {}
        self.state = {}

        self.frame, self.layout = create_widget_boxlayout()
        # self.frame.setStyleSheet("border: 1px solid green")
        self.content_frame, self.content_layout = create_widget_boxlayout(
            padding=[0, 0, 0, 0]
        )
        create_frame, create_layout = create_widget_boxlayout(layout="Horizontal")

        self.layout.addWidget(self.content_frame)
        self.layout.addWidget(create_frame)

        self.key = "None"
        button = QPushButton("Add key")
        button.clicked.connect(self.insert_wrapper)
        create_layout.addWidget(button, 0)
        self.line = QLineEdit()
        self.line.editingFinished.connect(self.set_key)
        create_layout.addWidget(self.line, 1)

        self.idx = 0

    def get_widget(self):
        return self.frame

    def insert_wrapper(self):
        self.insert_frame(self.key)

    def insert_frame(self, key, state=None):
        if key in self.saved:
            return
        args = copy.deepcopy(self.args)
        widget = self.builder.build_widget(input_definitions=args,
                                           definitions_depth=0,
                                           callback=self.dict_callback,
                                           parent=[key])

        self.saved[key] = widget
        generated, widget_layout = create_widget_boxlayout(
            padding=[10, 0, 0, 0])
        widget.populate_layout(widget_layout)

        header, h_layout = create_widget_boxlayout(layout="Horizontal")
        btn = QPushButton("-")
        btn.setMaximumWidth(btn.fontMetrics().boundingRect("-").width() * 6)
        call = self.remove_callback_builder(header, generated, key)
        btn.clicked.connect(call)
        h_layout.addWidget(btn)
        h_layout.addWidget(QLabel(key))

        # layout.addWidget(widget.get_widget())
        self.content_layout.addWidget(header)
        self.content_layout.addWidget(generated)
        self.idx += 1
        self.line.setText("")

    def set_value(self, value):
        pass

    def set_state(self, state):
        for key, value in state.items():
            self.insert_frame(key, value)

    def remove_callback_builder(self, header, frame, key):
        def remove_widget():
            frame.setParent(None)
            header.setParent(None)
            del self.saved[key]
        return remove_widget

    def dict_callback(self, path, value):
        if path[0] not in self.state:
            self.state[path[0]] = {}
        self.state[path[0]][path[1]] = value
        self.value_callback(self.state)

    def set_key(self):
        self.key = self.line.text()

    def get_value(self):
        values = {}
        for key, widget in self.saved.items():
            values[key] = widget.get_values()
        return values
