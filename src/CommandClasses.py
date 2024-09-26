# Standard library imports
from enum import Enum, auto
from wave import Error

# Third-party imports
import pyautogui as gui
import speech_recognition as sr
from word2number import w2n

# Local application imports
from src.SpeechRecognitionUtils import print_all_commands


class CommandType(Enum):
    """
    Enum representing the different types of commands that can be processed.

    Attributes:
        KEYBOARD (auto): Commands related to keyboard inputs.
        START_STOP (auto): Commands for starting or stopping typing activity.
        PROGRAMMING (auto): Commands related to programming actions.
        INFO (auto): Commands related to informational actions.
        SELECTION (auto): Commands related to text selection actions.
    """
    KEYBOARD = auto()
    START_STOP = auto()
    PROGRAMMING = auto()
    INFO = auto()
    SELECTION = auto()
    TERMINAL = auto()


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
        _execute_selection_command(text): Handles the execution of selection commands.
        _extract_num(text): Extracts and returns a numeric value from the text.
        numeric_str_to_int(numeric_str): Converts a numeric string to an integer.
    """
    def __init__(self, name, command_type, key=None, num_key=None):
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

    def execute(self, text, state):
        """
        Executes the command based on its type.

        Parameters:
            text (str): The command text.
            state (AppState): The current application state.

        Depending on the command type, this method will either execute a keyboard command,
        toggle typing activity, type out a programming or info command, or execute a selection command.
        """
        if self.command_type == CommandType.KEYBOARD:
            self._execute_keyboard_command(text)
        elif self.command_type == CommandType.START_STOP:
            self._execute_switch_commands(text, state)

        elif self.command_type == CommandType.PROGRAMMING:
            self.execute_programming_commands(text, state)

        elif self.command_type == CommandType.TERMINAL:
            self.execute_terminal_commands(text, state)

        elif self.command_type == CommandType.INFO:
            self._execute_info_command(text)

        elif self.command_type == CommandType.SELECTION:
            self._execute_selection_command(text)

    @staticmethod
    def set_typing_to_active(state):
        """
        Sets the typing activity to active in the application state.

        Parameters:
            state (AppState): The current application state object.

        This method sets the 'typing_active' attribute of the state object to True
        and prints the current status of the application state.
        """
        state.typing_active = True
        state.print_status()

    @staticmethod
    def _execute_switch_commands(text, state):
        """
        Executes switch commands based on the recognized text input.

        Parameters:
            text (str): The recognized text input.
            state (AppState): The current application state.

        This method handles various switch commands like toggling typing activity, restarting the script,
        enabling or disabling programming mode, and prints the current status of the application state.
        """
        if text == "go to sleep":
            state.typing_active = False
        if text == "wake up":
            state.typing_active = True
        elif text == "refresh texter":
            state.restart_script()
        elif text == "programming on":
            state.programming = True
        elif text == "programming off":
            state.programming = False
        elif text == "terminal on":
            state.terminal = True
        elif text == "terminal off":
            state.terminal = False

        state.print_status()

    def _execute_info_command(self, text):
        """
        Executes the information command based on the given text.

        Parameters:
            text (str): The recognized text input.

        If the text is 'print commands', it prints all available commands; otherwise, it types out the associated key.
        """
        if text == "print commands":
            print_all_commands()
        else:
            gui.typewrite(self.key)

    def _execute_keyboard_command(self, text):
        """
        Handles the execution of a keyboard command.

        Parameters:
            text (str): The command text.

        This method extracts a numeric value from the text (if present) to determine
        how many times to press the associated key.
        """
        n = text[len(self.num_key):]

        if ":" in n:
            try:
                num = int(n.split(":")[0])
            except ValueError:
                num = 1
        else:
            if text[len(self.num_key):].isdigit():
                num = int(text[len(self.num_key):])
            else:
                try:
                    num = self._extract_num(text[len(self.num_key):])
                except Error as e:
                    print(e)
                    num = 1
        for _ in range(num):
            gui.hotkey(self.key)

    @staticmethod
    def _execute_selection_command(text):
        """
        Handles the execution of a selection command.

        Parameters:
            text (str): The command text.

        This method performs actions such as selecting a line, selecting all text, deleting text,
        copying, or pasting based on the recognized command.
        """
        if text == "select line":
            gui.hotkey('home')
            gui.hotkey('shift', 'end')
        elif text == "select all":
            gui.hotkey('ctrl', 'a')
        elif text == "delete line":
            gui.hotkey('home')  # Assuming Home key will go to the beginning of the line
            gui.hotkey('shift', 'end', 'backspace')
        elif text == "delete all":
            gui.hotkey('ctrl', 'a', 'backspace')
        elif text == "copy":
            gui.hotkey('ctrl', 'c')
        elif text == "paste":
            gui.hotkey('ctrl', 'v')

    def execute_programming_commands(self, text, state):
        """
        Execute programming-related commands based on the user's selected programming language.

        Parameters:
        - text (str): The input text that may contain specific commands or additional details (e.g., class or method names).
        - state (object): An object containing the current state, including the selected programming language.

        This method performs different actions based on the `programming_language` attribute in the `state` object:
        - For Python, it can generate print statements, classes, methods, functions, variable declarations (int, str, float), and main script structures.
        - For Java, it supports creating print statements, classes, public/private methods, and functions.

        Commands are interpreted from `self.key` and may include actions like:
        - "print statement" for generating a print statement.
        - "create class", "create method", "create function" to generate respective components.
        - Type hints like "integer", "string", and "double" for generating type declarations.

        The method uses GUI automation (via `gui.typewrite` and `gui.hotkey`) to simulate typing the corresponding code
        structure in the editor.
        """
        if state.programming_language == "python":
            if self.key == "print statement":
                gui.typewrite("print()")
                gui.hotkey("left")
            elif self.key.startswith("create class"):
                class_name = text[len(self.key):]
                class_name = self.string_to_camel_case(class_name)
                gui.typewrite("class :")
                gui.hotkey("enter")
                gui.hotkey("tab")
                gui.typewrite("def __init__(self):")
                gui.hotkey("up")
                gui.hotkey("left")
                if len(class_name):
                    gui.typewrite(class_name)
            elif self.key.startswith("create method"):
                method_name = text[len(self.key):]
                method_name = self.string_to_snake_case(method_name)
                gui.typewrite("def (self):")
                for _ in range(0, 7):
                    gui.hotkey("left")
                if len(method_name):
                    gui.typewrite(method_name)
            elif self.key.startswith("create function"):
                function_name = self.string_to_snake_case(text[len(self.key):])
                gui.typewrite("def :()")
                for _ in range(0, 3):
                    gui.hotkey("left")
                if len(function_name):
                    gui.typewrite(function_name)
            elif self.key.startswith("new script"):
                gui.typewrite("main():")
                gui.hotkey("enter")
                gui.hotkey("enter")
                gui.typewrite("if __name__ == \"__main__\":")
                gui.hotkey("enter")
                gui.typewrite("main")
            elif self.key == "integer":
                gui.typewrite("int")
            elif self.key == "string":
                gui.typewrite("str")
            elif self.key == "double":
                gui.typewrite("float")
            else:
                gui.typewrite(self.key)

        elif state.programming_language == "java":
            if self.key == "print statement":
                gui.typewrite("System.out.println();")
                gui.hotkey("left")
                gui.hotkey("left")
            elif self.key.startswith("create class"):
                class_name = text[len(self.key):]
                class_name = self.string_to_camel_case(class_name)
                gui.typewrite("public class  {")
                gui.hotkey("enter")
                gui.hotkey("up")
                gui.hotkey("end")
                gui.hotkey("left")
                gui.hotkey("left")
                if len(class_name):
                    gui.typewrite(class_name)
            elif (self.key.startswith("create method") or self.key.startswith("create public method") or
                  self.key.startswith("create function") or self.key.startswith("create public function")):
                method_name = text[len(self.key):]
                method_name = self.string_to_snake_case(method_name)
                gui.typewrite("public void () {}")
                for _ in range(0, 5):
                    gui.hotkey("left")
                if len(method_name):
                    gui.typewrite(method_name)
            elif self.key.startswith("create private method") or self.key.startswith("create private function"):
                method_name = text[len(self.key):]
                method_name = self.string_to_snake_case(method_name)
                gui.typewrite("private void () {}")
                for _ in range(0, 5):
                    gui.hotkey("left")
                if len(method_name):
                    gui.typewrite(method_name)

            else:
                gui.typewrite(self.key)

    def execute_terminal_commands(self, text, state):
        """
        Execute terminal commands based on the user's selected operating system (OS).

        Parameters:
        - text (str): The input text that contains terminal commands or details (e.g., file paths or navigation commands).
        - state (object): An object containing the current state, including the selected terminal operating system (OS).

        This method checks the `terminal_os` attribute in the `state` object to determine the current OS:
        - If the OS is "linux", it will execute Linux-specific terminal commands.
        - If the OS is "windows", it will execute Windows-specific terminal commands.

        The method uses GUI automation (via `gui.typewrite`) to simulate typing the command in the terminal.
        """
        if state.terminal_os == "linux":
            if self.name == "go to":
                gui.typewrite(self.key)
        elif state. terminal_os == "windows":
            if self.name == "go to":
                gui.typewrite(self.key)

    @staticmethod
    def string_to_camel_case(input_str):
        """Capitalizes the first letter of each word in a string.

          Parameters:
            input_str: The input string.

          Returns:
            The string with the first letter of each word capitalized.
          """
        words = input_str.split()
        capitalized_words = [word.capitalize() for word in words]
        return "".join(capitalized_words)

    @staticmethod
    def string_to_snake_case(input_str):
        """
        Convert a given string to snake_case format.

        Parameters:
        - input_str (str): The input string to be converted, where words are typically separated by spaces.

        Returns:
        - str: The converted string in snake_case format, where spaces are replaced by underscores.
        """
        return input_str.replace(" ", "_")[1:]

    def _extract_num(self, text):
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
                return self.numeric_str_to_int(text)
        except (ValueError, sr.UnknownValueError):
            return 1

    @staticmethod
    def numeric_str_to_int(numeric_str):
        """
        Converts a numeric string to an integer.

        Parameters:
        - numeric_str (str): The numeric string (e.g., "three") to convert.

        Returns:
        - int: The corresponding integer value.
        """
        numeric_str = numeric_str.split(" ")
        nums = [str(w2n.word_to_num(w)) for w in numeric_str]
        return int(''.join(nums))