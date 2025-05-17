"""
This file defines constants, enums, and lists used for command processing.

It includes enumerations for different command types, programming languages,
and terminal operating systems, as well as a list of simple terminal command names.
"""
from enum import Enum, auto

window_height_in_pixels = 100


class CommandType(Enum):
    """
    Enum representing the different types of commands that can be processed.
    """
    KEYBOARD = auto()
    SWITCH = auto()
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
