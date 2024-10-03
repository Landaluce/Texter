# Standard library imports
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
        self.spelling = False
        self.typing_active = True
        self.terminate = False
        self.config = None

        self.keyboard_commands = []
        self.info_commands = []
        self.selection_commands = []

        self.programming = True
        self.programming_language = "python"  # None
        self.programming_commands = []

        self.terminal = True
        self.terminal_os = "linux"
        self.terminal_commands = []

        self.spelling_commands = None

        self.app_ui = app_ui

    def load_commands(self, config):
        """
        Loads all command from the given dictionary
        """
        self.config = config
        for i in config["keyboard_commands"]:
            if i["command_type"] == "keyboard":
                self.keyboard_commands.append(Command(i["name"], CommandType.KEYBOARD, i["key"], i["num_key"]))
            elif i["command_type"] == "start_stop":
                self.keyboard_commands.append(Command(i["name"], CommandType.START_STOP))

        self.info_commands = [
            Command(cmd["name"], CommandType.INFO, cmd["key"])
            for cmd in config["info_commands"]
        ]

        self.selection_commands = [
            Command(cmd["name"], CommandType.SELECTION)
            for cmd in config["selection_commands"]
        ]

        self.load_programming_commands()
        self.load_terminal_commands()
        self.load_spelling_commands()

    def load_programming_commands(self):
        """
        Loads programming commands for the specified language from the configuration file and sets the current language.

        Returns:
        - None: If programming in False
        """
        if not self.programming:
            return

        self.programming_commands = [
            Command(cmd.get("name", ""), CommandType.PROGRAMMING, cmd["key"], cmd.get("num_key", ""))
            for cmd in self.config[self.programming_language + "_commands"]
        ]
        self.print_status()

    def load_terminal_commands(self) -> None:
        """
        Loads terminal commands for the specified operating system from a configuration file and sets the current os.

        Returns:
        - None: If terminal in False
        """
        if not self.terminal:
            return

        self.terminal_commands = [
            Command(cmd.get("name", ""), CommandType.TERMINAL, cmd["key"])  #, cmd.get("num_key", ""))
            for cmd in self.config[self.terminal_os + "_commands"]
        ]
        self.print_status()

    def load_spelling_commands(self) -> None:
        """
        Loads spelling commands from a configuration file.
        """
        self.spelling_commands = [
            Command(cmd.get("name", ""), CommandType.SPELLING, cmd["key"], cmd.get("num_key", ""))
            for cmd in self.config["spelling_commands"]
        ]
        self.print_status()

    def handle_command(self, text):
        """
        Processes a given text command by checking it against different command types.

        Parameters:
        - text (str): The command text to process.

        Returns:
        - bool: True if a command was successfully handled, False otherwise.
        """
        # Try to handle as a keyboard command first
        if self._handle_keyboard_command(text):
            return True
        # Handle programming commands if applicable
        elif self._handle_programming_command(text):
            return True
        # Handle terminal commands if applicable
        elif self._handle_terminal_command(text):
            return True
        # Handle info commands if applicable
        elif self._handle_info_command(text):
            return True
        # Handle selection commands if applicable
        elif self._handle_selection_command(text):
            return True
        # Handle spelling commands if applicable
        elif self._handle_spelling_command(text):
            return True
        # Return False if no command matches
        return False

    def _handle_keyboard_command(self, text):
        """
        Handles a keyboard command if the text matches any of the available keyboard commands.

        Parameters:
            text (str): The command text to process.
        Returns:
            bool: True if a keyboard command was handled, False otherwise.
        """
        for command in self.keyboard_commands:
            if text.startswith(command.name):
                if command.name.startswith("switch to"):
                    language = command.name.split(" ")[-1]

                    if language == "python" or language == "java":
                        self.load_programming_commands()
                    elif language == "linux" or language == "windows":
                        self.load_terminal_commands()
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

    def _handle_info_command(self, text):
        """
        Handles an info command if the text matches any of the available info commands.

        Parameters:
            text (str): The command text to process.

        Returns:
            bool: True if an info command was handled, False otherwise.
        """
        for command in self.info_commands:
            if text.startswith(command.name):
                command.execute(text, self)
                return True
        return False

    def _handle_selection_command(self, text: str) -> bool:
        """
        Handles a selection command if the text matches any of the available selection commands.

        Parameters:
            text (str): The command text to process.

        Returns:
            bool: True if a selection command was handled, False otherwise.
        """
        for command in self.selection_commands:
            if text.startswith(command.name):
                command.execute(text, self)
                return True
        return False

    def _handle_spelling_command(self, text: str) -> bool:
        """
        Handles a spelling command if the text matches any of the available spelling commands.

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

    def print_status(self):
        """
        Prints the current status of typing activity, mode, terminal and programming language.
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
        elif self.mode == "spelling":
            self.mode = "dictation"
        self.print_status()

    @staticmethod
    def restart_script() -> None:
        subprocess.Popen([sys.executable, sys.argv[0]])
        sys.exit()
