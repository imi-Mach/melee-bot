from enum import Enum, auto

# may need an action queue to represent more complex actions (actions that are made up of a sequence of simple actions like wave dashing)

class Actions(Enum):
    PRESS_A = auto()
    PRESS_B = auto()
    PRESS_X = auto() 
    MAIN_STICK_RIGHT = auto()
    MAIN_STICK_LEFT = auto()

    