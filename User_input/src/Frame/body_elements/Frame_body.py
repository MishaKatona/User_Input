from ...Tools import create_widget_boxlayout


class FrameContainer:

    def __init__(self, args, value_callback, state_callback, parent_frame):
        self.callback = value_callback
        self.widget, self.layout = create_widget_boxlayout()
        self.state = {}

        builder = parent_frame.frame_builder

        self.w = builder.build_widget(input_definitions=args,
                                      definitions_depth=0,
                                      callback=self.dict_callback)

        self.w.populate_layout(self.layout)

    def add_frame(self, frame, arg):
        pass

    def set_value(self, value):
        self.w.set_values(value)

    def get_widget(self):
        return self.widget

    def get_value(self):
        return self.w.get_values()

    def dict_callback(self, path, value):
        self.callback(self.get_value())
