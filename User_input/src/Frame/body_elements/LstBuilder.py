from ...Tools import create_widget_boxlayout, QHLine
from PySide6.QtWidgets import QPushButton
from PySide6.QtCore import Qt
import copy

test_input = {
    "Layer Type": {"Type": "Choice",
                   "Options": ["Fully Connected",
                               "Convolution",
                               "Recurrent"]},
    "Neuron Count": {"Type": "int",
                     "SubSetting": {"Layer Type": "Fully Connected"}},
    "Activation Function": {"Type": "Choice",
                            "Body": False,
                            "Options": ["ReLu",
                                        "Sigmoid",
                                        "Binary",
                                        "Linear"]},
    "Kernel Size": {"Type": "int",
                    "SubSetting": {"Layer Type": "Convolution"}},
    "Stride": {"Type": "int",
               "SubSetting": {"Layer Type": "Convolution"}},
    "Recurrent Type": {"Type": "Choice",
                       "Options": ["LSTM", "GRU", "RNN"],
                       "Body": False,
                       "SubSetting": {"Layer Type": "Recurrent"}},
    "Dropout": {"Type": "int",
                "SubSetting": {"Layer Type": "Recurrent"}
                }
}

test_input2 = {
    "Type": None,
    "Label": {"Text": "Layer",
              "Bold": True},
    "InputItem": False,
    "Body": {"Widget": "Dict",
             "Indent": 15,
             "Expanded": True,
             "Args": {"Layer Type": {"Type": "Choice",
                                     "Options": ["Fully Connected",
                                                 "Convolution",
                                                 "Recurrent"]},
                      "Neuron Count": "int",
                      "Activation Function": {"Type": "Choice",
                                              "Options": ["ReLu",
                                                          "Sigmoid",
                                                          "Binary",
                                                          "Linear"]},
                      "Dropout": "int"
                      }
             }
}

test_input3 = {
    "Type": None,
    "Label": {"Text": "Layer",
              "Bold": True},
    "InputItem": False,
    "Body": {"Widget": "Dict",
             "Indent": 15,
             "Expanded": True,
             "Args": {"shit": "int"}
             }
}


# TODO for some reason when adding multiple (around 5) elements with expandable body
#  the first 1-5 stop working as some point
#  SOLUTION: this seems to be fixed by saving the frame explicitly within this class
class LstBuilder:

    def __init__(self, args, value_callback, state_callback, parent_frame):
        self.parent = parent_frame
        self.builder = parent_frame.frame_builder
        self.args = test_input
        self.saved = {}
        self.callback = value_callback

        self.frame, self.layout = create_widget_boxlayout()
        self.content, self.content_l = create_widget_boxlayout()

        button = QPushButton("new")
        button.clicked.connect(self.insert_frame)
        self.layout.addWidget(self.content)
        self.layout.addWidget(button, 0)

        self.idx = 1

    def insert_frame(self):
        args = copy.deepcopy(self.args)
        widget = self.builder.build_widget(input_definitions=args,
                                           definitions_depth=0,
                                           callback=self.lst_callback)

        self.saved[self.idx] = widget
        generated, widget_layout = create_widget_boxlayout(
            padding=[10, 0, 0, 0])
        widget.populate_layout(widget_layout)
        h_line = QHLine()

        header, h_layout = create_widget_boxlayout(layout="Horizontal")
        btn = QPushButton("-")
        btn.setMaximumWidth(btn.fontMetrics().boundingRect("-").width() * 6)
        call = self.remove_callback_builder(header, h_line, self.idx)
        btn.clicked.connect(call)
        h_layout.addWidget(btn, alignment=Qt.AlignTop)
        h_layout.addWidget(generated)

        # layout.addWidget(widget.get_widget())
        self.content_l.addWidget(header)

        self.saved[self.idx + 1] = h_line
        self.content_l.addWidget(h_line)
        self.idx += 2

    def set_value(self, value):
        for arg in value:
            self.insert_frame()
            self.saved[-1].set_value(arg)

    def set_state(self):
        pass

    def remove_callback_builder(self, frame, h_line, idx):
        def remove_widget():
            frame.setParent(None)
            h_line.setParent(None)
            del self.saved[idx + 1]
            del self.saved[idx]

        return remove_widget

    def lst_callback(self, path, value):
        self.callback(self.get_value())

    def get_value(self):
        lst = []
        for widget in self.saved.values():
            if hasattr(widget, "get_values"):
                lst.append(widget.get_values())
        return lst

    def get_widget(self):
        return self.frame
