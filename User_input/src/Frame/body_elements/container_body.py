from ...Tools import create_widget_boxlayout


class ContainerFrame:

    def __init__(self, args, value_callback, state_callback, parent_frame):
        self.widget, self.layout = create_widget_boxlayout()
        self.items = False

    def add_frame(self, frame, arg):
        self.layout.addWidget(frame.widget)
        self.items = True

    def get_widget(self):
        return self.widget

    def set_value(self, value):
        pass

    def get_value(self):
        return None

