"""
This module defines several Enums to categorize and represent different types of commands, programming languages, operating systems, and modes.

Enums:
- `CommandType`: Represents the different types of commands that can be processed.
    - `KEYBOARD`: Represents keyboard-related commands.
    - `SWITCH`: Represents switch commands.
    - `PROGRAMMING`: Represents programming commands.
    - `INFO`: Represents informational commands.
    - `SELECTION`: Represents selection commands.
    - `TERMINAL`: Represents terminal commands.
    - `SPELLING`: Represents spelling-related commands.
    - `GIT`: Represents git-related commands.
    - `INTERACTIVE`: Represents interactive commands.
    - `BROWSER`: Represents browser-related commands.

- `ProgrammingLanguage`: Represents different programming languages that can be processed.
    - `PYTHON`: Represents the Python programming language.
    - `JAVA`: Represents the Java programming language.

- `TerminalOS`: Represents the different operating systems that can be processed in terminal-related tasks.
    - `LINUX`: Represents the Linux operating system.
    - `WINDOWS`: Represents the Windows operating system.

- `Mode`: Represents different modes that can be processed.
    - `DICTATION`: Represents dictation mode.
    - `SPELLING`: Represents spelling mode.
"""
from enum import Enum, auto


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

class Mode(Enum):
    """
    Enum representing the different modes that can be processed.
    """
    DICTATION = "dictation"
    SPELLING = "spelling"