from ..src.Templates.Input_element_templates import input_elements
from ..src.Frame.body_elements.Body_elements import body_widget

all_input_keys = list(input_elements.keys())
all_body_widgets = list(body_widget.keys())

default_input_definition = {
    "DefaultTemplate": {
        "Label": {
            "Alignment": {"Type": "Choice",
                          "Options": ["Left", "Center", "Right", "Fill"],
                          "Body": False,
                          "Description": {"Text": "Sets alignment of the Label within Header"}},
            "Bold": {"Type": "bool",
                     "Description": {"Text": "If the Label text should be Bold"}},
            "Italic": {"Type": "bool",
                       "Description": {"Text": "If the Label text should be Italics"}},
            "MaxWidth": {"Type": "int",
                         "Description": {"Text": "Sets max width for Label"}},
            "IconSize": {"Type": "int",
                         "Description": {"Text": "Size of Icons next to the Label"}}
        },
        "InputItem": {
            "Type": {"Type": "Choice",
                     "Options": ["None"] + all_input_keys,
                     "Body": False,
                     "Description": {"Text": "PySide input element"}},
            "Location": {"Type": "Choice",
                         "Body": False,
                         "Options": ["Right", "Below"],
                         "Description": {"Text": "Place element with respect to Label"}},
            "Alignment": {"Type": "Choice",
                          "Body": False,
                          "Options": ["Left", "Center", "Right", "Fill"],
                          "Description": {"Text": "Sets alignment of the input element"}},
            "HideOnExpand": {"Type": "bool",
                             "Description": {"Text": "If it should be hidden on body expand"}}
        },
        "Description": {
            "Hover": {"Type": "bool",
                      "Description": {"Text": "If Description text should be in tooltip"}},
            "MaxWidth": {"Type": "int",
                         "Description": {"Text": "Max width of tooltip"}}
        },
        "Body": {
            "Widget": {"Type": "Choice",
                       "Options": ["None"] + all_body_widgets,
                       "Body": False,
                       "Description": {"Text": "Widget to use if none defined"}},
            "Expanded": {"Type": "bool",
                         "Description": {"Text": "If body should be expanded by default"}},
            "AlwaysExpanded": {"Type": "bool",
                               "Description": {"Text": "If it should always be expanded"}},
            "ExpandOnValue": {"Type": "bool",
                              "Description": {"Text": "If body should expand based on header value"}},
            "Indent": {"Type": "int",
                       "Description": {"Text": "Amount to indent body widget by"}},
        },
        "ExpandButton": {
            "Size": {"Type": "int",
                     "Description": {"Text": "Size of expand button"}},
            "Border": {"Type": "bool",
                       "Description": {"Text": "If it should have a border"}}
        },
        "Settings": {
            "AllowLock": {"Type": "bool",
                          "Description": {"Text": "If frame should be lockable"}}
        }
    },
    "BuildSettings": {
        "BuildSettings": {
            "AddSeparator": {"Type": "bool"},
            "Clustering": {"Type": "frame",
                           "Body": {
                               "Args": {"TabBy": {"Type": "Choice",
                                                  "Options": ["Tab", "Group",
                                                              [0, "Depth 0"],
                                                              [1, "Depth 1"],
                                                              [2, "Depth 2"]],
                                                  "Body": False},
                                        "GroupBy": {"Type": "Choice",
                                                    "Options": ["Group", "Tab",
                                                                [0, "Depth 0"],
                                                                [1, "Depth 1"],
                                                                [2, "Depth 2"]],
                                                    "Body": False},
                                        "DefaultTab": {"Type": "str"}
                                        }}},
        }
    }
}

# {"Clustering": {"TabBy": "Tab", "GroupBy": "Group",
#                                          "DefaultTab": "default"},
#                           "AddSeparator": True}
