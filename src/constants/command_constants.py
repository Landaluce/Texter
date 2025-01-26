from enum import Enum, auto

from src.utils.gui_utils import press, scroll

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


simple_terminal_command_names = ["view current directory", "list directory contents", "show network information",
                                "show system information", "check active processes", "show system information",
                                "clear terminal screen"]
selection_commands_map = {
    "select line": lambda: press("home", "shift", "end"),
    "select all": lambda: press("ctrl", "a"),
    "delete line": lambda: press("home", "shift", "end", "backspace"),
    "delete all": lambda: press("ctrl", "a", "backspace"),
    "copy": lambda: press("ctrl", "c"),
    "paste": lambda: press("ctrl", "v"),
}
browser_commands_map = {
    "browser right": lambda: press("ctrl", "tab"),
    "browser left": lambda: press("ctrl", "shift", "tab"),
    "new chrome window": lambda: press("ctrl", "n"),
    "new firefox window": lambda: press("ctrl", "n"),
    "new incognito window": lambda: press("ctrl", "n"),
    "go back": lambda: press("alt", "left"),
    "go forward": lambda: press("alt", "right"),
    "refresh page": lambda: press("ctrl", "r"),
    "stop refreshing": lambda: press("esc"),
    "scroll down": lambda: scroll(-window_height_in_pixels),
    "scroll up": lambda: scroll(window_height_in_pixels),
    "scroll to top": lambda: press("ctrl", "home"),
    "scroll to bottom": lambda: press("ctrl", "end"),
    "new tab": lambda: press("ctrl", "t"),
    "close tab": lambda: press("ctrl", "w"),
    "next tab": lambda: press("ctrl", "tab"),
    "previous tab": lambda: press("ctrl", "shift", "tab"),
    "reopen closed tab": lambda: press("ctrl", "shift", "t"),
    "close window": lambda: press("alt", "f4"),
    "minimize window": lambda: press("win", "down"),
    "maximize window": lambda: press("win", "up"),
    "open downloads": lambda: press("ctrl", "j"),
    "open history": lambda: press("ctrl", "h"),
    "open settings": lambda: (press("alt", "e"), press("s")),
    "zoom in": lambda: press("ctrl", "+"),
    "zoom out": lambda: press("ctrl", "-"),
    "reset zoom": lambda: press("ctrl", "0"),
    "bookmark page": lambda: press("ctrl", "d"),
    "print page": lambda: press("ctrl", "p"),
    "save page": lambda: press("ctrl", "s"),
}
