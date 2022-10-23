from PySide6.QtWidgets import QLabel


class Description:

    def __init__(self, parent_frame):
        self.parent = parent_frame
        self.template = parent_frame.template

        self.set_hover_tooltip_text()

        self.widget = None
        self.build_widget()

    def build_widget(self):
        if self.template["Description"] and not self.template["Description"]["Hover"]:
            self.widget = QLabel(self.template["Description"]["Text"])

    def set_hover_tooltip_text(self):
        text = self.parent.meta_data["PathStr"]
        if self.template["Description"] and \
                self.template["Description"]["Hover"]:
            text += "\n" + self.template["Description"]["Text"]
        issues = self.collect_issues()
        if issues:
            self.parent.set_label_warning(True)
            text += "\n" + issues
        self.parent.set_label_tooltip(text)

    def collect_issues(self):
        issues = []
        for header, items in self.parent.issues.items():
            if items:
                issues.append("\n" + self.padded(header + " Issues", 30, "-"))
                for issue in items:
                    issues.append("\n" + issue)

        return "".join(issues)

    @staticmethod
    def padded(string, desired_len, padder):
        rest = desired_len - len(string)
        front_pad = rest // 2
        end_pad = front_pad + rest % 2
        return "".join([padder] * front_pad + [string] + [padder] * end_pad)
