from .container_body import ContainerFrame
from .IntSlider import IntSlider
from .Color_picker import PickColor
from .DictBuilder import DictBuilder
from .Stacked_body import StackedFrame
from .Frame_body import FrameContainer
from .FloatSlider import FloatSlider
from .LstBuilder import LstBuilder

body_widget = {"Container": ContainerFrame,
               "intSlider": IntSlider,
               "colorPicker": PickColor,
               "dictBuilder": DictBuilder,
               "Stack": StackedFrame,
               "frame": FrameContainer,
               "floatSlider": FloatSlider,
               "listBuilder": LstBuilder}
