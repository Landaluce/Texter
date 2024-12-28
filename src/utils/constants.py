from enum import Enum, auto


class CommandType(Enum):
    """
    Enum representing the different types of commands that can be processed.
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


class ProgrammingLanguage(Enum):
    """
    Enum representing the different programming languages that can be processed.
    """
    PYTHON = "python"
    JAVA = "java"

class TerminalOS(Enum):
    """
    Enum representing the different OS that can be processed.
    """
    LINUX = "linux"
    WINDOWS = "windows"

class Mode(Enum):
    """
    Enum representing the different modes that can be processed.
    """
    DICTATION = "dictation"
    SPELLING = "spelling"