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

import subprocess
from wave import Error
import pyautogui as gui
from src.utils.constants import ProgrammingLanguage, TerminalOS
from src.utils.text_to_speech import text_to_speech
from src.utils.string_utils import (string_to_snake_case, string_to_camel_case, extract_number_from_string,
    numeric_str_to_int)
from src.utils.date_time_utils import (get_current_time, get_current_date, month_number_to_name, day_number_to_name,
                                       get_day_of_week)


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
        if self.key == "print statement":
            gui.write("print()")
            gui.hotkey("left")
        elif self.key.startswith("create class"):
            self._create_python_class()
        elif self.key.startswith("create method"):
            self._create_python_method()
        elif self.key.startswith("create function"):
            self._create_python_function()
        elif self.key.startswith("new script"):
            self._create_new_python_script()
        elif self.key == "integer":
            gui.write("int")
        elif self.key == "string":
            gui.write("str")
        elif self.key == "double":
            gui.write("float")
        else:
            gui.write(self.key)

    def _create_python_class(self) -> None:
        """Generates a Python class structure."""
        class_name = self.key[len("create class"):].strip()  # Extract class name
        class_name = string_to_camel_case(class_name)
        gui.write("class :")
        gui.hotkey("enter")
        gui.hotkey("tab")
        gui.write("def __init__(self):")
        gui.hotkey("up")
        gui.hotkey("left")
        if len(class_name):
            gui.write(class_name)

    def _create_python_method(self) -> None:
        """Generates a Python method structure."""
        method_name = self.key[len("create method"):].strip()  # Extract method name
        method_name = string_to_snake_case(method_name)
        gui.write("def (self):")
        for _ in range(0, 7):
            gui.hotkey("left")
        if len(method_name):
            gui.write(method_name)

    def _create_python_function(self) -> None:
        """Generates a Python function structure."""
        function_name = self.key[len("create function"):].strip()  # Extract function name
        function_name = string_to_snake_case(function_name)
        gui.write("def :()")
        for _ in range(0, 3):
            gui.hotkey("left")
        if len(function_name):
            gui.write(function_name)

    @staticmethod
    def _create_new_python_script() -> None:
        """Generates a Python script structure."""
        gui.write("main():")
        gui.hotkey("enter")
        gui.hotkey("enter")
        gui.write('if __name__ == "__main__":')
        gui.hotkey("enter")
        gui.write("main")

    def _execute_java_command(self) -> None:
        """Handles Java-specific commands."""
        if self.key == "print statement":
            gui.write("System.out.println();")
            gui.hotkey("left")
            gui.hotkey("left")
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
            gui.write(self.key)

    def _create_java_class(self) -> None:
        """Generates a Java class structure."""
        class_name = self.key[len("create class"):].strip()  # Extract class name
        class_name = string_to_camel_case(class_name)
        gui.write("public class  {")
        gui.hotkey("enter")
        gui.hotkey("up")
        gui.hotkey("end")
        gui.hotkey("left")
        gui.hotkey("left")
        if len(class_name):
            gui.write(class_name)

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
        method_name = self.key[len("create " + access_level + " "):].strip()  # Extract method name
        method_name = string_to_snake_case(method_name)
        gui.write(access_level + " void () {}")
        for _ in range(0, 5):
            gui.hotkey("left")
        if len(method_name):
            gui.write(method_name)


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
                    print(e)
                    num = 1
        for _ in range(num):
            gui.hotkey(self.key)


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
        command_map = {
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

        if self.name in command_map:
            command_map[self.name]()
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
        gui.write(self.key)


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
        gui.write(self.key)


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
        simple_command_names = ["view current directory", "list directory contents", "show network information",
                                "show system information", "check active processes", "show system information",
                                "clear terminal screen"]
        if ((self.name.startswith("change permissions") and app_state.terminal_os == TerminalOS.LINUX) or
                self.name.startswith("go to")):
            gui.write(self.key)
        elif self.name in simple_command_names:
            gui.write(self.key)
            gui.hotkey("enter")
        else:
            pass #gui.write(self.key)


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
        commands = {
            "select line": lambda: gui.hotkey("home", "shift", "end"),
            "select all": lambda: gui.hotkey("ctrl", "a"),
            "delete line": lambda: gui.hotkey("home", "shift", "end", "backspace"),
            "delete all": lambda: gui.hotkey("ctrl", "a", "backspace"),
            "copy": lambda: gui.hotkey("ctrl", "c"),
            "paste": lambda: gui.hotkey("ctrl", "v"),
        }

        command_executed = commands.get(self.name)
        if self.name in commands:
            command_executed()
        else:
            print(f"Unknown command: {self.name}")


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
        command_mapping = {
            "browser right": lambda: gui.hotkey("ctrl", "tab"),
            "browser left": lambda: gui.hotkey("ctrl", "shift", "tab"),
            "new chrome window": lambda: gui.hotkey("ctrl", "n"),
            "new firefox window": lambda: gui.hotkey("ctrl", "n"),
            "new incognito window": lambda: gui.hotkey("ctrl", "n"),
            "focus chrome": lambda: self.focus_browser_window(),
            "focus firefox": lambda: self.focus_browser_window("Firefox"),
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

        if self.name.startswith("browser"):
            if "right" in self.name:
                gui.hotkey("Ctrl", "Tab")
            elif "left" in self.name or "lyft" in self.name:
                gui.hotkey("Ctrl", "Shift", "Tab")
            else:
                try:
                    num_str = self.name.split(" ")[1].strip()
                    if not num_str.isdigit():
                        num_str = str(numeric_str_to_int(num_str))
                    gui.hotkey("ctrl", num_str)
                except (ValueError, IndexError):
                    pass
        else:
            # Match specific command strings to their actions
            for command, action in command_mapping.items():
                if self.name.startswith(command):
                    action()
                    break

    @staticmethod
    def start_browser(browser="chrome", url=None) -> None:
        """
        Starts Chrome or Firefox browser. Optionally opens a specific URL.

        Args:
            browser (str): Either "chrome" or "firefox".
            url (str): Optional URL to open in the browser.
        """
        try:
            if browser.lower() == "chrome":
                command = ["google-chrome"]
            elif browser.lower() == "firefox":
                command = ["firefox"]
            else:
                print("Unsupported browser. Use 'chrome' or 'firefox'.")
                return

            # Add URL to command if provided
            if url:
                command.append(url)

            # Run the command
            subprocess.Popen(command)
            print(f"Started {browser} successfully.")
        except FileNotFoundError:
            print(f"Error: {browser.capitalize()} is not installed or not in PATH.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def focus_browser_window(self, browser="Chrome") -> None:
        """
        Attempts to focus an existing browser window based on the provided name.

        Args:
            browser (str, optional): The name of the browser window to focus. Defaults to "Chrome".
        """
        try:
            # Search for the browser window
            result = subprocess.run(
                ["xdotool", "search", "--name", browser],
                capture_output=True,
                text=True
            )
            window_id = result.stdout.splitlines()[0]  # Get the first matching window ID

            # Focus the window
            subprocess.run(["xdotool", "windowactivate", window_id])
        except IndexError:
            text_to_speech(f"No open {browser} window found. starting {browser}")
            self.start_browser(browser)
        except Exception as e:
            print(f"Error: {e}")
