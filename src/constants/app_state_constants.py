from enum import Enum

from src.constants.command_constants import CommandType

command_groups = {
    "keyboard_commands": CommandType.KEYBOARD,
    "info_commands": CommandType.INFO,
    "selection_commands": CommandType.SELECTION,
    "switch_commands": CommandType.SWITCH,
    "spelling_commands": CommandType.SPELLING,
    "git_commands": CommandType.GIT,
    "interactive_commands": CommandType.INTERACTIVE,
    "browser_commands": CommandType.BROWSER,
}


class Mode(Enum):
    """
    Enum representing the different modes that can be processed.
    """
    DICTATION = "dictation"
    SPELLING = "spelling"
