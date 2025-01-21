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
import pyautogui as gui


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


simple_terminal_command_names = ["view current directory", "list directory contents", "show network information",
                                "show system information", "check active processes", "show system information",
                                "clear terminal screen"]

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

selection_commands_map = {
    "select line": lambda: gui.hotkey("home", "shift", "end"),
    "select all": lambda: gui.hotkey("ctrl", "a"),
    "delete line": lambda: gui.hotkey("home", "shift", "end", "backspace"),
    "delete all": lambda: gui.hotkey("ctrl", "a", "backspace"),
    "copy": lambda: gui.hotkey("ctrl", "c"),
    "paste": lambda: gui.hotkey("ctrl", "v"),
}

browser_commands_map = {
    "browser right": lambda: gui.hotkey("ctrl", "tab"),
    "browser left": lambda: gui.hotkey("ctrl", "shift", "tab"),
    "new chrome window": lambda: gui.hotkey("ctrl", "n"),
    "new firefox window": lambda: gui.hotkey("ctrl", "n"),
    "new incognito window": lambda: gui.hotkey("ctrl", "n"),
    "go back": lambda: gui.hotkey("alt", "left"),
    "go forward": lambda: gui.hotkey("alt", "right"),
    "refresh page": lambda: gui.hotkey("ctrl", "r"),
    "stop refreshing": lambda: gui.press("esc"),
    "scroll down": lambda: gui.scroll(-100),
    "scroll up": lambda: gui.scroll(100),
    "scroll to top": lambda: gui.hotkey("ctrl", "home"),
    "scroll to bottom": lambda: gui.hotkey("ctrl", "end"),
    "new tab": lambda: gui.hotkey("ctrl", "t"),
    "close tab": lambda: gui.hotkey("ctrl", "w"),
    "next tab": lambda: gui.hotkey("ctrl", "tab"),
    "previous tab": lambda: gui.hotkey("ctrl", "shift", "tab"),
    "reopen closed tab": lambda: gui.hotkey("ctrl", "shift", "t"),
    "close window": lambda: gui.hotkey("alt", "f4"),
    "minimize window": lambda: gui.hotkey("win", "down"),
    "maximize window": lambda: gui.hotkey("win", "up"),
    "open downloads": lambda: gui.hotkey("ctrl", "j"),
    "open history": lambda: gui.hotkey("ctrl", "h"),
    "open settings": lambda: (gui.hotkey("alt", "e"), gui.press("s")),
    "zoom in": lambda: gui.hotkey("ctrl", "+"),
    "zoom out": lambda: gui.hotkey("ctrl", "-"),
    "reset zoom": lambda: gui.hotkey("ctrl", "0"),
    "bookmark page": lambda: gui.hotkey("ctrl", "d"),
    "print page": lambda: gui.hotkey("ctrl", "p"),
    "save page": lambda: gui.hotkey("ctrl", "s"),
}
