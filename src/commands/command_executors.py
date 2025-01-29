"""
Module that defines classes for executing various types of commands in a GUI.
The classes support programming, keyboard, terminal, selection, switch, and interactive commands.

Each command executor corresponds to a specific action, such as typing programming commands (Python/Java),
executing terminal commands, simulating keyboard actions, switching app states, or interacting with the browser.
The primary function of each class is to simulate user interactions within a graphical interface.

Classes:
    - ProgrammingCommandExecutor: Executes programming commands for Python and Java.
    - KeyboardCommandExecutor: Executes keyboard-related commands such as hotkeys and key presses.
    - SwitchCommandExecutor: Executes commands to switch application states (e.g., programming mode, terminal mode).
    - InfoCommandExecutor: Executes info commands that simply type text into the GUI.
    - GitCommandExecutor: Executes Git-related commands within the terminal or GUI.
    - TerminalCommandExecutor: Executes terminal-related commands such as navigating directories or system commands.
    - SelectionCommandExecutor: Executes commands to manipulate selected text (e.g., copy, paste, delete).
    - InteractiveCommandExecutor: Executes interactive commands, including fetching and reading out the time or date.
    - BrowserCommandExecutor: Executes browser-related commands such as switching tabs, opening windows, and navigating pages.

Each executor is initialized with a command key or name and can be invoked to simulate a GUI interaction.
"""

from wave import Error
from src.utils.gui_utils import press, write
from src.utils.command_utils import focus_browser_window
from src.constants.command_constants import (ProgrammingLanguage, TerminalOS, simple_terminal_command_names,
                                             selection_commands_map, browser_commands_map)
from src.utils.text_to_speech import text_to_speech
from src.utils.string_utils import string_to_camel_case, extract_number_from_string, numeric_str_to_int
from src.utils.date_time_utils import (get_current_time, get_current_date, month_number_to_name, day_number_to_name,
                                       get_day_of_week)
import logging
from logging_config import setup_logging
setup_logging()
warning_logger = logging.getLogger('warning_logger')
error_logger = logging.getLogger('error_logger')


class ProgrammingCommandExecutor:
    """
    A class that executes programming commands within a graphical user interface (GUI).

    This class takes a key (representing the programming command) as input during initialization
    and provides methods to execute the corresponding programming actions based on the selected
    programming language (currently supports Python and Java).
    """

    def __init__(self, key: str):
        """
        Initializes a new ProgrammingCommand instance.

        Args:
            key (str): The key associated with the programming command.
        """
        self.key = key

    def execute(self, app_state) -> None:
        """
        Executes the programming command based on the selected language.

        Args:
            app_state (AppState): The current application state object containing the selected programming language.
        """
        if app_state.programming_language == ProgrammingLanguage.PYTHON:
            self._execute_python_command()
        elif app_state.programming_language == ProgrammingLanguage.JAVA:
            self._execute_java_command()

    def _execute_python_command(self) -> None:
        """Handles Python-specific commands."""
        python_commands_map = {
            "print statement": lambda: (write("print()"), press("left")),
            "integer": lambda: write("int"),
            "string": lambda: write("str"),
            "double": lambda: write("float"),
            "create class": self._create_python_class,
            "create method": self._create_python_method,
            "create function": self._create_python_function,
            "new script": self._create_new_python_script,
        }

        # Execute the corresponding function or default to writing the key
        command_action = python_commands_map.get(self.key, lambda: write(self.key))
        command_action()

    def _extract_name_from_key(self, input_str: str):
        name = self.key[len(input_str)].strip()  # Extract class name
        return string_to_camel_case(name)

    def _create_python_class(self) -> None:
        """Generates a Python class structure."""
        class_name = self._extract_name_from_key("create class")
        write("class :")
        press("enter")
        press("tab")
        write("def __init__(self):")
        press("up")
        press("left")
        if len(class_name):
            write(class_name)

    def _create_python_method(self) -> None:
        """Generates a Python method structure."""
        method_name = self._extract_name_from_key("create method")
        write("def (self):")
        for _ in range(0, 7):
            press("left")
        if len(method_name):
            write(method_name)

    def _create_python_function(self) -> None:
        """Generates a Python function structure."""
        function_name = self._extract_name_from_key("create function")
        write("def :()")
        for _ in range(0, 3):
            press("left")
        if len(function_name):
            write(function_name)

    @staticmethod
    def _create_new_python_script() -> None:
        """Generates a Python script structure."""
        write("main():")
        press("enter")
        press("enter")
        write('if __name__ == "__main__":')
        press("enter")
        write("main")

    def _execute_java_command(self) -> None:
        """Handles Java-specific commands."""
        if self.key == "print statement":
            write("System.out.println();")
            press("left")
            press("left")
        elif self.key.startswith("create class"):
            self._create_java_class()
        elif (
                self.key.startswith("create method")
                or self.key.startswith("create public method")
                or self.key.startswith("create function")
                or self.key.startswith("create public function")
        ):
            self._create_java_public_method()
        elif (
                self.key.startswith("create private method")
                or self.key.startswith("create private function")
        ):
            self._create_java_private_method()
        else:
            write(self.key)

    def _create_java_class(self) -> None:
        """Generates a Java class structure."""
        class_name = self._extract_name_from_key("create class")
        write("public class  {")
        press("enter")
        press("up")
        press("end")
        press("left")
        press("left")
        if len(class_name):
            write(class_name)

    def _create_java_public_method(self) -> None:
        """Generates a Java public method structure."""
        self._create_java_method("public")

    def _create_java_private_method(self) -> None:
        """Generates a Java private method structure."""
        self._create_java_method("private")

    def _create_java_method(self, access_level: str) -> None:
        """
        Generates a Java method structure based on the specified access level.

        This method extracts the method name from the command key, constructs the
        method declaration with the given access level (e.g., "public", "private"), and
        positions the cursor for further editing.

        Args:
            access_level (str): The access level of the method (e.g., "public", "private").
        """
        method_name = self._extract_name_from_key("create " + access_level + " ")
        write(access_level + " void () {}")
        for _ in range(0, 5):
            press("left")
        if len(method_name):
            write(method_name)


class KeyboardCommandExecutor:
    """
    Represents a command that can be executed to generate keyboard keystrokes.
    """

    def __init__(self, key: str, name, num_key: str = None):
        """
        Initializes a new KeyboardCommand instance.

        Args:
            key (str): The key to be pressed.
            num_key (str, optional): The key used for repeatable commands.
        """
        self.key = key
        self.num_key = num_key
        self.name = name

    def execute(self) -> None:
        """
        Executes the keyboard command.
        """
        n = self.name[len(self.num_key):]

        if ":" in n:
            try:
                num = int(n.split(":")[0])
            except ValueError:
                num = 1
        else:
            if self.name[len(self.num_key):].isdigit():
                num = int(self.name[len(self.num_key):])
            else:
                try:
                    num = extract_number_from_string(self.name[len(self.num_key):])
                except Error as e:
                    error_logger.error(e)
                    num = 1
        for _ in range(num):
            press(self.key)


class SwitchCommandExecutor:
    """
    Represents a command that switches application states.
    """

    def __init__(self, name: str):
        """
        Initializes a new SwitchCommand instance.

        Args:
            name (str): The name of the switch command.
        """
        self.name = name

    def execute(self, app_state) -> None:
        """
        Executes the switch command.

        Args:
            app_state (AppState): The current application state.
        """
        switch_command_map = {
            "go to sleep": lambda: setattr(app_state, "typing_active", False),
            "wake up": lambda: setattr(app_state, "typing_active", True),
            "refresh texter": app_state.restart_script,
            "programming on": lambda: setattr(app_state, "programming", True),
            "programming off": lambda: setattr(app_state, "programming", False),
            "terminal on": lambda: setattr(app_state, "terminal", True),
            "terminal off": lambda: setattr(app_state, "terminal", False),
            "switch mode": lambda: app_state.switch_mode(),
            "switch punctuation": lambda: app_state.switch_punctuation(),
            "switch caps": lambda: app_state.switch_capitalization(),
            "switch cups": lambda: app_state.switch_capitalization(), # TODO: find better way to fix
            "switch to java": lambda: (app_state.set_programming_language(ProgrammingLanguage.JAVA),
                                       app_state.load_programming_commands()),
            "switch to python": lambda: (app_state.set_programming_language(ProgrammingLanguage.PYTHON),
                                       app_state.load_programming_commands()),
            "switch to windows": lambda: (app_state.set_terminal_os(TerminalOS.WINDOWS),
                                       app_state.load_terminal_commands()),
            "switch to linux": lambda: (app_state.set_terminal_os(TerminalOS.LINUX),
                                       app_state.load_terminal_commands()),
        }

        if self.name in switch_command_map:
            switch_command_map[self.name]()
            app_state.update_status()


class InfoCommandExecutor:
    """
    Executes an info command.

    Args:
        key (str): The key to be typed.
    """
    def __init__(self, key: str):
        """
        Initializes an InfoCommandExecutor instance.

        Args:
            key (str): The key to be typed.
        """
        self.key = key

    def execute(self) -> None:
        """
        Executes the info command.
        """
        write(self.key)


class GitCommandExecutor:
    """
    Executes a Git command by typing the specified key.

    Args:
        key (str): The key associated with the Git command.
        """
    def __init__(self, key: str):
        """
        Initializes a GitCommandExecutor instance.

        Args:
            key (str): The key associated with the Git command.
        """
        self.key = key

    def execute(self) -> None:
        """
        Executes the info command.
        """
        write(self.key)


class TerminalCommandExecutor:
    """
    A class that executes selection commands within a GUI.
    """

    def __init__(self, key: str, name: str):
        """
        Initializes a `TerminalCommandExecutor` instance.

        Args:
            name (str): The name of the selection command to be executed.
        """
        self.key = key
        self.name = name

    def execute(self, app_state) -> None:
        """
        Executes a terminal command.

        Args:
            app_state (AppState): The current application state, including information about the terminal OS.
        """
        if ((self.name.startswith("change permissions") and app_state.terminal_os == TerminalOS.LINUX) or
                self.name.startswith("go to")):
            write(self.key)
        elif self.name in simple_terminal_command_names:
            write(self.key)
            press("enter")
        else:
            pass #write(self.key)


class SelectionCommandExecutor:
    """
    A class that executes selection commands within a GUI.

    This class takes a command name as input during initialization and provides an `execute` method
    to perform the corresponding selection action. Supported commands include selecting a line,
    selecting all text, deleting text, copying, and pasting.
    """
    def __init__(self, name: str):
        """
        Initializes a `SelectionCommandExecutor` instance.

        Args:
            name (str): The name of the selection command to be executed.
        """
        self.name = name

    def execute(self) -> None:
        """
        Handles the execution of a selection command.

        This method performs actions such as selecting a line, selecting all text, deleting text,
        copying, or pasting based on the recognized command.
        """
        command_executed = selection_commands_map.get(self.name)
        if self.name in selection_commands_map:
            command_executed()
        else:
            error_logger.error(f"Unknown command: {self.name}")


class InteractiveCommandExecutor:
    """
    A class that executes interactive commands within a GUI.
    """

    def __init__(self, name: str):
        """
        Initializes a `SelectionCommandExecutor` instance.

        Args:
            name (str): The name of the selection command to be executed.
        """
        self.name = name

    def execute(self) -> None:
        """
        Executes the interactive command.
        """
        if self.name.startswith("what time is it") or self.name.startswith("what's the time"):
            current_time = get_current_time()
            text_to_speech("it's " + current_time)
        elif self.name.startswith("what's the date"):
            current_date_time = get_current_date()

            month_day = current_date_time.strftime("%m-%d")
            date = month_day.split("-")
            month = month_number_to_name(int(date[0]))
            day = day_number_to_name(int(date[1]))

            y_m_d = str(current_date_time.strftime("%Y-%m-%d"))
            week_day = get_day_of_week(y_m_d)

            current_date = f"{week_day}, {month} {day}"
            text_to_speech(current_date)
        else:
            text_to_speech("no input")


class BrowserCommandExecutor:
    """
    A class that executes browser commands within a GUI.
    """
    def __init__(self, name: str):
        """
        Initializes a `SelectionCommandExecutor` instance.

        Args:
            name (str): The name of the selection command to be executed.
        """
        self.name = name

    def execute(self) -> None:
        """
        Executes the interactive command.
        """
        browser_commands = browser_commands_map
        # Handle instance-specific logic
        browser_commands["focus chrome"] = lambda: focus_browser_window()
        browser_commands["focus firefox"] = lambda: focus_browser_window("Firefox")


        if self.name.startswith("browser"):
            if "right" in self.name:
                press("Ctrl", "Tab")
            elif "left" in self.name or "lyft" in self.name:
                press("Ctrl", "Shift", "Tab")
            else:
                try:
                    num_str = self.name.split(" ")[1].strip()
                    if not num_str.isdigit():
                        num_str = str(numeric_str_to_int(num_str))
                    press("ctrl", num_str)
                except (ValueError, IndexError):
                    pass
        else:
            for command, action in browser_commands_map.items():
                if self.name.startswith(command):
                    action()
                    break
