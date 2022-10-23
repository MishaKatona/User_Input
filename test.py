from User_input.UI_stand_alone import build_window
from math import sqrt

values = build_window({"Side 1": {"Type": "intS"},
                       "Side 2": {"Type": "intS"}},
                      0)

print(f"Triangle with sides {values['Side 1']}, {values['Side 2']} "
      f"give a hypotenuse of "
      f"{sqrt(values['Side 1'] ** 2 + values['Side 2'] ** 2)}")
