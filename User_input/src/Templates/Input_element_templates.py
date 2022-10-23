from json import JSONDecodeError

from PySide6.QtWidgets import QSpinBox, QCheckBox, QComboBox, \
    QDoubleSpinBox, QLineEdit, QAbstractSpinBox, QTextEdit, QSlider, QDateEdit, \
    QDateTimeEdit, QTimeEdit
from PySide6.QtCore import Qt
from .Input_elements.QTextEdit import TextEdit
from .Input_elements.QDoubleSlider import DoubleSlider
import json


def date_formatter(date):
    return date.toPython(), date


def dict_formatter(dict_str):
    try:
        dict_obj = json.loads(dict_str)
        return dict_obj, json.dumps(dict_obj, indent=4, sort_keys=False)
    except JSONDecodeError:
        return dict_str, dict_str


def lst_formatter(lst_str):
    try:
        lst_obj = json.loads(lst_str)
        return lst_obj, str(lst_obj)
    except:
        print("not formatted")
        return lst_str, lst_str


def dict_set_formatter(obj):
    # returns the formatted object and if there were any issues
    if type(obj) == str:
        return obj, False
    elif type(obj) == dict:
        return json.dumps(obj), False


# If an input setting receives a setting value of type bool
# then it will influence if that setting gets applied
# TODO add Set attribute and logic to choice

input_elements = {
    "bool": {"Widget": QCheckBox, "Set": "setChecked",
             "Get": "isChecked", "Change": "stateChanged"},
    "int": {"Widget": QSpinBox, "Set": "setValue",
            "Get": "value", "Change": "valueChanged",
            "Settings": {"Range": {"PysideCall": "setRange",
                                   "Default": [-2147483648, 2147483647],
                                   "Hint": "[min:int, max:int]",
                                   "Description": "Set minimum and maximum "
                                                  "value of int input element"},
                         "AdaptiveStep": {"PysideCall": "setStepType",
                                          "Default": QAbstractSpinBox.AdaptiveDecimalStepType,
                                          "Hint": "bool",
                                          "Description": "Set step size to be dynamic "
                                                         "with respect to the value"}}},
    "float": {"Widget": QDoubleSpinBox, "Set": "setValue",
              "Get": "value", "Change": "valueChanged",
              "Settings": {"Range": {"PysideCall": "setRange",
                                     "Default": [-2147483648, 2147483647],
                                     "Hint": "[min:float, max:float]",
                                     "Description": "Set minimum and maximum "
                                                    "value of float input element"},
                           "Decimals": {"PysideCall": "setDecimals",
                                        "Default": 2,
                                        "Hint": "decimal places:int",
                                        "Description": "Set the number of decimal places "
                                                       "that can be entered"},
                           "AdaptiveStep": {"PysideCall": "setStepType",
                                            "Default": QAbstractSpinBox.AdaptiveDecimalStepType,
                                            "Hint": "bool",
                                            "Description": "Set step size to be dynamic "
                                                           "with respect to the value"}}},
    "Choice": {"Widget": QComboBox, "Get": "currentText",
               "Change": "currentIndexChanged", "Set": "setCurrentIndex"},
    "strLine": {"Widget": QLineEdit, "Set": "setText",
                "Get": "text", "Change": "editingFinished"},
    "strText": {"Widget": TextEdit, "Set": "setPlainText",
                "Get": "toPlainText"},
    "intSlider": {"Widget": QSlider, "Set": "setValue",
                  "Get": "value", "Change": "sliderMoved",
                  "Input": {"orientation": Qt.Horizontal},
                  "Settings": {"Min": {"PysideCall": "setMinimum",
                                       "Default": -100,
                                       "Hint": "min:int",
                                       "Description": "Set minimum value of slider"},
                               "Max": {"PysideCall": "setMaximum",
                                       "Default": 100,
                                       "Hint": "max:int",
                                       "Description": "Set maximum value of slider"},
                               "Range": {"PysideCall": "setRange",
                                         "Default": [0, 100],
                                         "Hint": "[min:float, max:float]",
                                         "Description": "Set minimum and maximum "
                                                        "value of float input element"},
                               },
                  "Setters": {"setMin": "setMinimum", "setMax": "setMaximum"}},
    "floatSlider": {"Widget": DoubleSlider, "Set": "setValue",
                    "Get": "value", "Change": "sliderMoved",
                    "Input": {"Decimals": 3, "Orientation": Qt.Horizontal},
                    "Settings": {"Min": {"PysideCall": "setMinimum",
                                         "Default": -100,
                                         "Hint": "min:int",
                                         "Description": "Set minimum value of slider"},
                                 "Max": {"PysideCall": "setMaximum",
                                         "Default": 100,
                                         "Hint": "max:int",
                                         "Description": "Set maximum value of slider"},
                                 "Range": {"PysideCall": "setRange",
                                           "Default": [0, 100],
                                           "Hint": "[min:float, max:float]",
                                           "Description": "Set minimum and maximum "
                                                          "value of float input element"},
                                 },
                    "Setters": {"setMin": "setMinimum", "setMax": "setMaximum",
                                "setRange": "setRange"}},
    "dateTime": {"Widget": QDateTimeEdit, "Set": "setDateTime",
                 "Get": "dateTime", "Change": "dateTimeChanged",
                 "Input": {"calendarPopup": True},
                 "Settings": {"Format": {"PysideCall": "setDisplayFormat",
                                         "Default": "yyyy-M-d HH:mm:ss.zzz",
                                         "Hint": "format:str",
                                         "Description": "Set display format "
                                                        "y - M - d - H - M - s - z "
                                                        "for year to millisecond"}},
                 "Format": date_formatter},
    "date": {"Widget": QDateEdit, "Set": "setDate",
             "Get": "date", "Change": "dateChanged",
             "Input": {"calendarPopup": True},
             "Settings": {"Format": {"PysideCall": "setDisplayFormat",
                                     "Default": "yyyy-M-d",
                                     "Hint": "format:str",
                                     "Description": "Set display format "
                                                     "y - M - d "
                                                    "for year to day"}},
             "Format": date_formatter},
    "time": {"Widget": QTimeEdit, "Set": "setTime",
             "Get": "time", "Change": "timeChanged",
             "Settings": {"Format": {"PysideCall": "setDisplayFormat",
                                     "Default": "HH:mm:ss.zzz",
                                     "Hint": "format:str",
                                     "Description": "Set display format "
                                                    "H - M - s - z "
                                                    "for hour to millisecond"}},
             "Format": date_formatter},
    "dict": {"Widget": TextEdit, "Set": "setPlainText",
             "Get": "toPlainText", "Format": dict_formatter,
             "SetFormatter": dict_set_formatter,
             "Input": {"max_lines": 4}},
    "list": {"Widget": TextEdit, "Set": "setPlainText",
             "Get": "toPlainText",
             "Format": lst_formatter},
}
