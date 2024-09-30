# Standard library imports
import json
import subprocess
import sys

# Local application imports
from src.CommandClasses import CommandType, Command

class AppState:
    """
    Represents the state of the application, including typing status,
    the current programming language, and associated commands.

    Attributes:
        typing_active (bool): Indicates whether typing is currently active.
        programming_language (str): The currently selected programming language.
        programming_commands (list): A list of commands associated with the selected programming language.
    """
    def __init__(self, app_ui=None):
        """
        Initializes a new instance of the AppState class with default settings.
        """
        self.mode = "dictation"
        # self.spelling = False
        self.typing_active = True
        self.terminate = False

        self.programming = True
        self.programming_language = "python"  # None
        self.programming_commands = []

        self.terminal = True
        self.terminal_os = "linux"
        self.terminal_commands = []

        self.spelling_commands = None

        self.app_ui = app_ui
        self.load_programming_commands(self.programming_language, "config.json")
        self.load_terminal_commands(self.terminal_os, "config.json")
        self.load_spelling_commands("config.json")

    @staticmethod
    def load_commands(config):
        """
        Loads all command types (keyboard, info, selection) from a configuration file.

        Returns:
            tuple: A tuple containing lists of keyboard commands, info commands, and selection commands.
        """
        keyboard_commands = []
        for i in config["keyboard_commands"]:
            if i["command_type"] == "keyboard":
                keyboard_commands.append(Command(i["name"], CommandType.KEYBOARD, i["key"], i["num_key"]))
            elif i["command_type"] == "start_stop":
                keyboard_commands.append(Command(i["name"], CommandType.START_STOP))

        info_commands = [
            Command(cmd["name"], CommandType.INFO, cmd["key"])
            for cmd in config["info_commands"]
        ]

        selection_commands = [
            Command(cmd["name"], CommandType.SELECTION)
            for cmd in config["selection_commands"]
        ]

        return keyboard_commands, info_commands, selection_commands

    def load_programming_commands(self, language, config_file_path):
        """
        Loads programming commands for the specified language from a configuration file and sets the current language.

        Parameters:
        - language (str): The programming language for which to load commands.
        - config_file_path (str): The path to the configuration JSON file containing the programming commands.

        Returns:
        - None: If the configuration file is not found or contains errors.
        """
        if not self.programming:
            return
        try:
            with open(config_file_path, 'r') as f:
                config = json.load(f)
        except FileNotFoundError:
            print("Configuration file not found.")
            return None
        except json.JSONDecodeError:
            print("Invalid JSON format in configuration file.")
            return None
        self.programming_commands = [
            Command(cmd.get("name", ""), CommandType.PROGRAMMING, cmd["key"], cmd.get("num_key", ""))
            for cmd in config[language + "_commands"]
        ]
        self.programming_language = language
        self.print_status()

    def load_terminal_commands(self, os: str, config_file_path: str) -> None:
        """
        Loads terminal commands for the specified operating system from a configuration file and sets the current os.

        Parameters:
            config_file_path (str): The path of the json file the terminal command.
            os (str): The operating system for which to load commands.
        """
        if not self.terminal:
            return
        try:
            with open(config_file_path, 'r') as f:
                config = json.load(f)
        except FileNotFoundError:
            print("Configuration file not found.")
            return None
        except json.JSONDecodeError:
            print("Invalid JSON format in configuration file.")
            return None
        self.terminal_commands = [
            Command(cmd.get("name", ""), CommandType.TERMINAL, cmd["key"]) #, cmd.get("num_key", ""))
            for cmd in config[os + "_commands"]
        ]
        self.terminal_os = os
        self.print_status()

    def load_spelling_commands(self, config_file_path: str) -> None:
        """
        Loads spelling commands from a configuration file.

        Parameters:
            config_file_path (str): The path of the json file the spelling command.
        """
        try:
            with open(config_file_path, 'r') as f:
                config = json.load(f)
        except FileNotFoundError:
            print("Configuration file not found.")
            return None
        except json.JSONDecodeError:
            print("Invalid JSON format in configuration file.")
            return None
        self.spelling_commands = [
            Command(cmd.get("name", ""), CommandType.SPELLING, cmd["key"], cmd.get("num_key", ""))
            for cmd in config["spelling_commands"]
        ]
        self.print_status()

    def handle_command(self, text, keyboard_commands, info_commands, selection_commands):
        """
        Processes a given text command by checking it against different command types.

        Parameters:
        - text (str): The command text to process.
        - keyboard_commands (list): List of keyboard commands.
        - info_commands (list): List of info commands.
        - selection_commands (list): List of selection commands.

        Returns:
        - bool: True if a command was successfully handled, False otherwise.
        """
        # Try to handle as a keyboard command first
        if self._handle_keyboard_command(text, keyboard_commands, "config.json"):
            return True
        # Handle programming commands if applicable
        elif self._handle_programming_command(text):
            return True
        # Handle terminal commands if applicable
        elif self._handle_terminal_command(text):
            return True
        # Handle info commands if applicable
        elif self._handle_info_command(text, info_commands):
            return True
        # Handle selection commands if applicable
        elif self._handle_selection_command(text, selection_commands):
            return True
        # Handle spelling commands if applicable
        elif self._handle_spelling_command(text):
            return True
        # Return False if no command matches
        return False

    def _handle_keyboard_command(self, text, keyboard_commands, config_file_path):
        """
        Handles a keyboard command if the text matches any of the available keyboard commands.

        Parameters:
            text (str): The command text to process.
            keyboard_commands (list): List of keyboard commands.
            config_file_path (str): The path of the json file the spelling command.
        Returns:
            bool: True if a keyboard command was handled, False otherwise.
        """
        for command in keyboard_commands:
            if text.startswith(command.name):
                if command.name.startswith("switch to"):
                    language = command.name.split(" ")[-1]

                    if language == "python" or language == "java":
                        self.load_programming_commands(language, config_file_path)
                    elif language == "linux" or language == "windows":
                        self.load_terminal_commands(language, config_file_path)
                else:
                    command.execute(text, self)
                return True
        return False

    def _handle_programming_command(self, text: str) -> bool:
        """
        Handles a programming command if the text matches any of the available programming commands.

        Parameters:
            text (str): The command text to process.

        Returns:
            bool: True if a programming command was handled, False otherwise.
        """
        if not self.programming:
            return False
        for command in self.programming_commands:
            if text.startswith(command.name):
                command.execute_programming_command(text, self)
                return True
        return False

    def _handle_terminal_command(self, text: str) -> bool:
        """
        Handles a terminal command if the text matches any of the available terminal commands.

        Parameters:
            text (str): The command text to process.

        Returns:
            bool: True if a terminal command was handled, False otherwise.
        """
        if not self.terminal:
            return False
        for command in self.terminal_commands:
            if text.startswith(command.name):
                command.execute_terminal_command(text, self)
                return True
        return False

    def _handle_info_command(self, text, info_commands):
        """
        Handles an info command if the text matches any of the available info commands.

        Parameters:
            text (str): The command text to process.
            info_commands (list): List of info commands.

        Returns:
            bool: True if an info command was handled, False otherwise.
        """
        for command in info_commands:
            if text.startswith(command.name):
                command.execute(text, self)
                return True
        return False

    def _handle_selection_command(self, text: str, selection_commands) -> bool:
        """
        Handles a selection command if the text matches any of the available selection commands.

        Parameters:
            text (str): The command text to process.
            selection_commands (list): List of selection commands.

        Returns:
            bool: True if a selection command was handled, False otherwise.
        """
        for command in selection_commands:
            if text.startswith(command.name):
                command.execute(text, self)
                return True
        return False

    def _handle_spelling_command(self, text: str) -> bool:
        """
        Handles a spelling command if the text matches any of the available terminal commands.

        Parameters:
            text (str): The command text to process.

        Returns:
            bool: True if a spelling command was handled, False otherwise.
        """
        if self.mode == "spelling":
            for command in self.spelling_commands:
                if text.startswith(command.name):
                    command.execute_spelling_command(self, text)
                    return True
        return False

    def print_status(self, texter_ui=None):
        """
        Prints the current status of typing activity and programming language.
        If app_ui is passed, it will update the TexterUI status box.
        """
        status_message = f"Typing: {'started' if self.typing_active else 'stopped'}\n"
        status_message += f"mode: {self.mode}\n"
        status_message += f"{self.programming_language} Programming: On\n" if self.programming else "Programming: Off\n"
        status_message += f"{self.terminal_os} Terminal: On\n" if self.terminal else "Terminal: Off\n"

        # Check if app_ui is available and update UI
        if self.app_ui:
            self.app_ui.update_status(status_message)
        else:
            print(status_message)

    def switch_mode(self):
        """Toggle between dictation and spelling modes."""
        if self.mode == "dictation":
            self.mode = "spelling"
            print("Switched to spelling mode")
        elif self.mode == "spelling":
            self.mode = "dictation"
            print("Switched to dictation mode")
        self.print_status()

    @staticmethod
    def restart_script() -> None:
        subprocess.Popen([sys.executable, sys.argv[0]])
        sys.exit()
