import sys
import subprocess
from src.commands.command_manager import CommandManager
from src.utils.constants import CommandType, ProgrammingLanguage, TerminalOS, Mode


class AppState:
    """
    Represents the state of the application, including typing status,
    the current programming language, and associated commands.

    Attributes:
        typing_active (bool): Indicates whether typing is currently active.
        programming_language (str): The currently selected programming language.
        programming_commands (list): A list of commands associated with the selected programming language.
        ...
    """

    def __init__(self, app_ui=None):
        """
        Initializes a new instance of the AppState class with default settings.
        """
        self.mode = Mode.DICTATION
        self.spelling = False
        self.typing_active = True
        self.terminate = False
        self.commands = None

        self.keyboard_commands = []
        self.info_commands = []
        self.selection_commands = []

        self.programming = True
        self.programming_language = ProgrammingLanguage.PYTHON
        self.programming_commands = []

        self.terminal = True
        self.terminal_os = TerminalOS.LINUX
        self.terminal_commands = []

        self.spelling_commands = None

        self.punctuation = False
        self.capitalize = False

        self.git_commands = []
        self.interactive_commands = []
        self.browser_commands = []

        self.app_ui = app_ui

    def load_commands(self, commands: dict) -> None:
        """
        Loads all command from the given dictionary
        """
        self.commands = commands
        for i in commands["keyboard_commands"]:
            if i["command_type"] == "keyboard":
                self.keyboard_commands.append(
                    CommandManager(i["name"], CommandType.KEYBOARD, i["key"], i["num_key"])
                )
            elif i["command_type"] == "start_stop":
                self.keyboard_commands.append(
                    CommandManager(i["name"], CommandType.START_STOP)
                )
        try:
            self.info_commands = [
                CommandManager(cmd["name"], CommandType.INFO, cmd["key"])
                for cmd in commands["info_commands"]
            ]
        except KeyError:
            print("Could not find info commands")

        self.selection_commands = [
            CommandManager(cmd["name"], CommandType.SELECTION)
            for cmd in commands["selection_commands"]
        ]

        self.load_programming_commands()
        self.load_terminal_commands()
        self.load_spelling_commands()
        self.load_git_commands()
        self.load_interactive_commands()
        self.load_browser_commands()

    def load_programming_commands(self) -> None:
        """
        Loads programming commands for the specified language from the commands file and sets the current language.
        """
        if not self.programming:
            return

        self.programming_commands = [
            CommandManager(
                cmd.get("name", ""),
                CommandType.PROGRAMMING,
                cmd["key"],
                cmd.get("num_key", ""),
            )
            for cmd in self.commands[self.programming_language.value + "_commands"]
        ]
        self.print_status()

    def load_terminal_commands(self) -> None:
        """
        Loads terminal commands for the specified operating system from the commands file and sets the current os.
        """
        if not self.terminal:
            return

        self.terminal_commands = [
            CommandManager(
                cmd.get("name", ""), CommandType.TERMINAL, cmd["key"]
            )  # , cmd.get("num_key", ""))
            for cmd in self.commands[self.terminal_os.value + "_commands"]
        ]
        self.print_status()

    def load_spelling_commands(self) -> None:
        """
        Loads spelling commands from the commands file.
        """
        self.spelling_commands = [
            CommandManager(
                cmd.get("name", ""),
                CommandType.SPELLING,
                cmd["key"],
                cmd.get("num_key", ""),
            )
            for cmd in self.commands["spelling_commands"]
        ]
        self.print_status()

    def load_git_commands(self) -> None:
        """
        Loads spelling commands from the commands file.
        """
        self.git_commands = [
            CommandManager(
                cmd.get("name", ""),
                CommandType.SPELLING,
                cmd["key"],
                cmd.get("num_key", ""),
            )
            for cmd in self.commands["git_commands"]
        ]
        self.print_status()

    def load_interactive_commands(self) -> None:
        """
        Loads spelling commands from the commands file.
        """
        self.interactive_commands = [
            CommandManager(
                cmd.get("name"),
                CommandType.INTERACTIVE,
                cmd["key"]
            )
            for cmd in self.commands["interactive_commands"]
        ]
        self.print_status()

    def load_browser_commands(self) -> None:
        """
        Loads spelling commands from the commands file.
        """
        self.browser_commands = [
            CommandManager(
                cmd.get("name"),
                CommandType.BROWSER,
                cmd["key"]
            )
            for cmd in self.commands["browser_commands"]
        ]

    def handle_command(self, text: str) -> bool:
        """
        Processes a given text command by checking it against different command types.

        Parameters:
        - text (str): The command text to process.

        Returns:
        - bool: True if a command was successfully handled, False otherwise.
        """
        command_handlers = [
            self._handle_keyboard_command,
            self._handle_programming_command,
            self._handle_terminal_command,
            self._handle_info_command,
            self._handle_selection_command,
            self._handle_spelling_command,
            self._handle_git_command,
            self._handle_interactive_command,
            self._handle_browser_command
        ]
        for handler in command_handlers:
            # noinspection PyArgumentList
            if handler(text):
                return True
        return False

    def _handle_keyboard_command(self, text: str) -> bool:
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
                    if language == ProgrammingLanguage.JAVA:
                        self.programming_language = ProgrammingLanguage.JAVA
                        self.load_programming_commands()
                    elif language == ProgrammingLanguage.PYTHON:
                        self.programming_language = ProgrammingLanguage.PYTHON
                        self.load_programming_commands()
                    elif language == TerminalOS.LINUX:
                        self.terminal_os = TerminalOS.LINUX
                        self.load_terminal_commands()
                    elif language == TerminalOS.WINDOWS:
                        self.terminal_os = TerminalOS.WINDOWS
                        self.load_terminal_commands()
                else:
                    command.execute(self)
                return True
        return False

    def _handle_git_command(self, text: str) -> bool:
        """
        Handles a git command if the text matches any of the available git commands.

        Parameters:
            text (str): The command text to process.

        Returns:
            bool: True if a programming command was handled, False otherwise.
        """
        for command in self.git_commands:
            if text.startswith(command.name):
                command.git_command_executor.execute()
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
                command.programming_command_executor.execute(self)
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
                command.terminal_command_executor.execute(self)
                return True
        return False

    def _handle_info_command(self, text: str) -> bool:
        """
        Handles an info command if the text matches any of the available info commands.

        Parameters:
            text (str): The command text to process.

        Returns:
            bool: True if an info command was handled, False otherwise.
        """
        for command in self.info_commands:
            if text.startswith(command.name):
                command.execute(self)
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
                command.execute(self)
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
        for command in self.spelling_commands:
            if text.startswith(command.name):
                command.execute_spelling_command(self)
                return True
        return False

    def _handle_interactive_command(self, text: str) -> bool:
        """
        Handles an interactive command if the text matches any of the available interactive commands.

        Parameters:
            text (str): The command text to process.

        Returns:
            bool: True if a spelling command was handled, False otherwise.
        """
        for command in self.interactive_commands:
            if text.startswith(command.name):
                command.terminal_command_executor.execute()
                return True
        return False

    def _handle_browser_command(self, text: str) -> bool:
        """
        Handles a browser command if the text matches any of the available interactive commands.

        Parameters:
            text (str): The command text to process.

        Returns:
            bool: True if a spelling command was handled, False otherwise.
        """
        for command in self.browser_commands:
            if text.startswith(command.name):
                command.browser_command_executor.execute()
                return True
        return False

    def print_status(self) -> None:
        """
        Prints the current status of typing activity, mode, terminal and programming language.
        """
        status_message = f"Typing: {'started' if self.typing_active else 'stopped'}\n"
        status_message += f"Mode: {self.mode.value}\n"
        status_message += (
            f"Programming: On  | {self.programming_language.value.capitalize()}\n"
            if self.programming
            else f"Programming: Off | {self.programming_language.value.capitalize()}\n"
        )
        status_message += (
            f"Terminal: On | {self.terminal_os.value}\n" if self.terminal else "Terminal: Off\n"
        )
        status_message += (
            f"Punctuation: On  " if self.punctuation else "Punctuation: Off "
        )
        status_message += f"| Caps: On" if self.capitalize else "| Caps: Off\n"

        # Check if app_ui is available and update UI
        if self.app_ui:
            self.app_ui.update_status(status_message)
            self.app_ui.update_commands()
        else:
            print(status_message)

    def switch_mode(self) -> None:
        """Toggle between dictation and spelling modes."""
        if self.mode == Mode.DICTATION:
            self.mode = Mode.SPELLING
        elif self.mode == Mode.SPELLING:
            self.mode = Mode.DICTATION
        self.print_status()

    def switch_typing(self) -> None:
        """Toggle typing On/OFF."""
        if self.typing_active:
            self.typing_active = False
        else:
            self.typing_active = True
        self.print_status()

    @staticmethod
    def restart_script() -> None:
        """Restart the currently running script."""
        subprocess.Popen([sys.executable, sys.argv[0]])
        sys.exit()
