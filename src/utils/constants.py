"""
This module defines several Enums, mappings, and utility constants to categorize and process various command types,
programming languages, operating systems, modes, and command mappings.

### Contents:

1. **Enums**:
   - `CommandType`: Represents the different types of commands that can be processed.
       - `KEYBOARD`: Keyboard-related commands.
       - `SWITCH`: Commands to toggle or switch settings.
       - `PROGRAMMING`: Commands specific to programming tasks.
       - `INFO`: Informational commands.
       - `SELECTION`: Commands for text selection and manipulation.
       - `TERMINAL`: Commands for terminal interactions.
       - `SPELLING`: Spelling-related commands.
       - `GIT`: Commands for Git version control tasks.
       - `INTERACTIVE`: Commands for interactive operations.
       - `BROWSER`: Browser-related commands.

   - `ProgrammingLanguage`: Represents supported programming languages.
       - `PYTHON`: Represents the Python programming language.
       - `JAVA`: Represents the Java programming language.

   - `TerminalOS`: Represents supported operating systems for terminal commands.
       - `LINUX`: Represents the Linux operating system.
       - `WINDOWS`: Represents the Windows operating system.

   - `Mode`: Represents operational modes for the application.
       - `DICTATION`: Dictation mode for processing spoken input.
       - `SPELLING`: Spelling mode for spelling out words.

2. **Mappings**:
   - `command_groups`: Maps command group names to their corresponding `CommandType`.
   - `selection_commands_map`: Maps selection-related commands to their corresponding `pyautogui` actions.
   - `browser_commands_map`: Maps browser-related commands to their corresponding `pyautogui` actions.

3. **Constants**:
   - `simple_terminal_command_names`: A list of common terminal command names for basic operations.
   - `replacements`: A dictionary of common text replacements for correcting recognition errors.

### Examples:

- **Command Group Mapping**:
    ```python
    command_groups["keyboard_commands"]  # Returns CommandType.KEYBOARD
    ```

- **Selection Command Execution**:
    ```python
    selection_commands_map["select all"]()  # Executes the keyboard shortcut to select all text.
    ```

- **Browser Command Execution**:
    ```python
    browser_commands_map["refresh page"]()  # Refreshes the current browser tab.
    ```

- **Replacement Application**:
    ```python
    text = "wright turn"
    corrected_text = text.replace("wright", "right")
    ```
"""
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

replacements = {
    "dexter": "texter",
    "texture": "texter",
    "lift": "left",
    "wright": "right",
}
