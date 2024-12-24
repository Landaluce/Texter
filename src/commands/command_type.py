from enum import Enum, auto


class CommandType(Enum):
    """
    Enum representing the different types of commands that can be processed.

    Attributes:
        KEYBOARD (auto): Commands related to keyboard inputs.
        START_STOP (auto): Commands for starting or stopping typing activity.
        PROGRAMMING (auto): Commands related to programming actions.
        INFO (auto): Commands related to informational actions.
        SELECTION (auto): Commands related to text selection actions.
        GIT (auto): Commands related to git
    """

    KEYBOARD = auto()
    START_STOP = auto()
    PROGRAMMING = auto()
    INFO = auto()
    SELECTION = auto()
    TERMINAL = auto()
    SPELLING = auto()
    GIT = auto()
    INTERACTIVE = auto()
    BROWSER = auto()