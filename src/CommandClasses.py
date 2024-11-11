# Standard library imports
from enum import Enum, auto
from wave import Error

# Third-party imports
import pyautogui as gui
import speech_recognition as sr

# Local application imports
from src.helperFunctions import (
    string_to_snake_case,
    string_to_camel_case,
    numeric_str_to_int,
    convert_to_spelling,
)


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
    GIT = auto


class Command:
    """
    Represents a command that can be executed based on recognized speech input.

    Attributes:
        name (str): The name of the command.
        command_type (CommandType): The type of command (e.g., KEYBOARD, START_STOP).
        key (str, optional): The key to be pressed for keyboard or programming commands.
        num_key (str, optional): The key used for commands that can be repeated multiple times.

    Methods:
        execute(text, state): Executes the command based on its type.
        _execute_keyboard_command(text): Handles the execution of keyboard commands.
        _execute_selection_command(): Handles the execution of selection commands.
        _extract_num(text): Extracts and returns a numeric value from the text.
        numeric_str_to_int(numeric_str): Converts a numeric string to an integer.
    """

    def __init__(self, name: str, command_type: CommandType, key=None, num_key=None):
        """
        Initializes a new Command instance.

        Parameters:
            name (str): The name of the command.
            command_type (CommandType): The type of command.
            key (str, optional): The key associated with the command.
            num_key (str, optional): The key used for repeatable commands.
        """
        self.name = name
        self.command_type = command_type
        self.key = key
        self.num_key = num_key

    def execute(self, text: str, app_state) -> None:
        """
        Executes the command based on its type.

        Parameters:
            text (str): The command text.
            app_state (AppState): The current application state.

        Depending on the command type, this method will either execute a keyboard command,
        toggle typing activity, type out a programming or info command, or execute a selection command.
        """

        if self.command_type == CommandType.KEYBOARD:
            self._execute_keyboard_command()

        elif self.command_type == CommandType.START_STOP:
            self._execute_switch_commands(app_state)

        elif self.command_type == CommandType.INFO:
            self._execute_info_command()

        elif self.command_type == CommandType.PROGRAMMING:
            self.execute_programming_command(app_state)

        elif self.command_type == CommandType.TERMINAL:
            self.execute_terminal_command(app_state)

        elif self.command_type == CommandType.SELECTION:
            self._execute_selection_command()

        elif self.command_type == CommandType.SPELLING:
            self.execute_spelling_command(app_state, text)

        elif self.command_type == CommandType.GIT:
            self.execute_git_command()

    # @staticmethod
    def _execute_switch_commands(self, app_state) -> None:
        """
        Executes switch commands based on the recognized text input.

        Parameters:
            app_state (AppState): The current application state.

        This method handles various switch commands like toggling typing activity, restarting the script,
        enabling or disabling programming mode, and prints the current status of the application state.
        """
        if self.name == "go to sleep":
            app_state.typing_active = False
        elif self.name == "wake up":
            app_state.typing_active = True
        elif self.name == "refresh texter":
            app_state.restart_script()
        elif self.name == "programming on":
            app_state.programming = True
        elif self.name == "programming off":
            app_state.programming = False
        elif self.name == "terminal on":
            app_state.terminal = True
        elif self.name == "terminal off":
            app_state.terminal = False
        elif self.name == "switch mode":
            app_state.switch_mode()

        app_state.print_status()

    def _type_command_key(self) -> None:
        """
        Types the stored key.
        """
        gui.write(self.key)

    def execute_git_command(self) -> None:
        self._type_command_key()

    def _execute_info_command(self) -> None:
        self._type_command_key()

    def _execute_keyboard_command(self) -> None:
        """
        Handles the execution of a keyboard command.

        This method extracts a numeric value from the text (if present) to determine
        how many times to press the associated key.
        """

        n = self.name[len(self.num_key) :]

        if ":" in n:
            try:
                num = int(n.split(":")[0])
            except ValueError:
                num = 1
        else:
            if self.name[len(self.num_key) :].isdigit():
                num = int(self.name[len(self.num_key) :])
            else:
                try:
                    num = self._extract_num(self.name[len(self.num_key) :])
                except Error as e:
                    print(e)
                    num = 1
        for _ in range(num):
            gui.hotkey(self.key)

    # @staticmethod
    def _execute_selection_command(self) -> None:
        """
        Handles the execution of a selection command.

        This method performs actions such as selecting a line, selecting all text, deleting text,
        copying, or pasting based on the recognized command.
        """
        if self.name == "select line":
            gui.hotkey("home")
            gui.hotkey("shift", "end")
        elif self.name == "select all":
            gui.hotkey("ctrl", "a")
        elif self.name == "delete line":
            gui.hotkey("home")  # Assuming Home key will go to the beginning of the line
            gui.hotkey("shift", "end", "backspace")
        elif self.name == "delete all":
            gui.hotkey("ctrl", "a", "backspace")
        elif self.name == "copy":
            gui.hotkey("ctrl", "c")
        elif self.name == "paste":
            gui.hotkey("ctrl", "v")

    def execute_programming_command(self, app_state) -> None:
        """
        Execute programming-related commands based on the user's selected programming language.

        Parameters:
        - app_state (object): An object containing the current state, including the selected programming language.

        This method performs different actions based on the `programming_language` attribute in the `state` object:
        - For Python, it can generate print statements, classes, methods, functions, variable declarations
            (int, str, float), and main script structures.
        - For Java, it supports creating print statements, classes, public/private methods, and functions.

        Commands are interpreted from `self.key` and may include actions like:
        - "print statement" for generating a print statement.
        - "create class", "create method", "create function" to generate respective components.
        - Type hints like "integer", "string", and "double" for generating type declarations.

        The method uses GUI automation (via `gui.write` and `gui.hotkey`) to simulate typing the corresponding code
        structure in the editor.
        """
        if app_state.programming_language == "python":
            if self.key == "print statement":
                gui.write("print()")
                gui.hotkey("left")
            elif self.key.startswith("create class"):
                class_name = self.name[len(self.key):]
                class_name = string_to_camel_case(class_name)
                gui.write("class :")
                gui.hotkey("enter")
                gui.hotkey("tab")
                gui.write("def __init__(self):")
                gui.hotkey("up")
                gui.hotkey("left")
                if len(class_name):
                    gui.write(class_name)
            elif self.key.startswith("create method"):
                method_name = self.name[len(self.key):].strip()
                method_name = string_to_snake_case(method_name)
                gui.write("def (self):")
                for _ in range(0, 7):
                    gui.hotkey("left")
                if len(method_name):
                    gui.write(method_name)
            elif self.key.startswith("create function"):
                function_name = string_to_snake_case(self.name[len(self.key):].strip())
                gui.write("def :()")
                for _ in range(0, 3):
                    gui.hotkey("left")
                if len(function_name):
                    gui.write(function_name)
            elif self.key.startswith("new script"):
                gui.write("main():")
                gui.hotkey("enter")
                gui.hotkey("enter")
                gui.write('if __name__ == "__main__":')
                gui.hotkey("enter")
                gui.write("main")
            elif self.key == "integer":
                gui.write("int")
            elif self.key == "string":
                gui.write("str")
            elif self.key == "double":
                gui.write("float")
            else:
                gui.write(self.key)

        elif app_state.programming_language == "java":
            if self.key == "print statement":
                gui.write("System.out.println();")
                gui.hotkey("left")
                gui.hotkey("left")
            elif self.key.startswith("create class"):
                class_name = self.name[len(self.key):]
                class_name = string_to_camel_case(class_name)
                gui.write("public class  {")
                gui.hotkey("enter")
                gui.hotkey("up")
                gui.hotkey("end")
                gui.hotkey("left")
                gui.hotkey("left")
                if len(class_name):
                    gui.write(class_name)
            elif (
                    self.key.startswith("create method")
                    or self.key.startswith("create public method")
                    or self.key.startswith("create function")
                    or self.key.startswith("create public function")
            ):
                method_name = self.name[len(self.key):].strip()
                method_name = string_to_snake_case(method_name)
                gui.write("public void () {}")
                for _ in range(0, 5):
                    gui.hotkey("left")
                if len(method_name):
                    gui.write(method_name)
            elif self.key.startswith("create private method") or self.key.startswith(
                    "create private function"
            ):
                method_name = self.name[len(self.key):].strip()
                method_name = string_to_snake_case(method_name)
                gui.write("private void () {}")
                for _ in range(0, 5):
                    gui.hotkey("left")
                if len(method_name):
                    gui.write(method_name)

            else:
                gui.write(self.key)

    def execute_terminal_command(self, app_state):
        """
        Execute terminal commands based on the user's selected operating system (OS).

        Parameters:
        - text (str): The input text that contains terminal commands or details
            (e.g., file paths or navigation commands).
        - app_state (object): An object containing the current state, including the selected terminal operating system (OS).

        This method checks the `terminal_os` attribute in the `state` object to determine the current OS:
        - If the OS is "linux", it will execute Linux-specific terminal commands.
        - If the OS is "windows", it will execute Windows-specific terminal commands.

        The method uses GUI automation (via `gui.write`) to simulate typing the command in the terminal.
        """
        if app_state.terminal_os == "linux":
            if self.name.startswith("go to"):
                gui.write(self.key)
        elif app_state.terminal_os == "windows":
            if self.name == "go to":
                gui.write(self.key)

    def execute_spelling_command(self, app_state, text=None):
        gui.write(self.key)
        spelling_output = convert_to_spelling(self.name, app_state.spelling_commands)
        if spelling_output:
            gui.write(spelling_output)
        else:
            app_state.append_text("No valid spelling commands found.")

    @staticmethod
    def _extract_num(text):
        """
        Extracts and returns a numeric value from the command text.

        Parameters:
        - text (str): The command text from which to extract the number.

        Returns:
        - int: The extracted numeric value, or 1 if extraction fails due to parsing errors.
        """
        try:
            if ":" in text:
                return int(text.split(":")[0])
            elif text.isdigit():
                return int(text)
            else:
                return numeric_str_to_int(text)
        except (ValueError, sr.UnknownValueError):
            return 1
