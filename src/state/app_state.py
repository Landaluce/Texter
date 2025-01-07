import sys
import subprocess
from src.commands.command_manager import CommandManager
from src.utils.constants import CommandType, ProgrammingLanguage, TerminalOS, Mode


class AppState:
    """
    Represents the state of the application, including typing status,
    the current programming language, and associated commands.

    Attributes:
        mode (Mode): Current application mode (e.g., DICTATION, SPELLING).
        typing_active (bool): Indicates whether typing is currently active.
        terminate (bool): Signals if the application should terminate.
        commands (dict): A dictionary of command configurations.
        programming (bool): Indicates if programming mode is enabled.
        programming_language (ProgrammingLanguage): The currently selected programming language.
        terminal (bool): Indicates if terminal commands are enabled.
        terminal_os (TerminalOS): The operating system for terminal commands.
        app_ui: Optional UI object for updating application status.
    """

    def __init__(self, app_ui=None):
        self.mode = Mode.DICTATION
        self.typing_active = True
        self.terminate = False
        self.commands = None

        self.programming = True
        self.programming_language = ProgrammingLanguage.PYTHON
        self.terminal = True
        self.terminal_os = TerminalOS.LINUX

        self.app_ui = app_ui

        #Command groups
        self.switch_commands = []
        self.keyboard_commands = []
        self.info_commands = []
        self.selection_commands = []
        self.programming_commands = []
        self.terminal_commands = []
        self.spelling_commands = []
        self.git_commands = []
        self.interactive_commands = []
        self.browser_commands = []

        # Additional settings
        self.spelling = False
        self.punctuation = False
        self.capitalize = False

    def load_commands(self, commands: dict) -> None:
        """Loads all command groups from the given dictionary."""
        self.commands = commands
        self.keyboard_commands = self._load_commands(commands.get("keyboard_commands", []), CommandType.KEYBOARD)
        self.info_commands = self._load_commands(commands.get("info_commands", []), CommandType.INFO)
        self.selection_commands = self._load_commands(commands.get("selection_commands", []), CommandType.SELECTION)
        self.switch_commands = self._load_commands(commands.get("switch_commands", []), CommandType.SWITCH)
        self.programming_commands = self._load_commands(
            commands.get(f"{self.programming_language.value}_commands", []), CommandType.PROGRAMMING
        ) if self.programming else []
        self.terminal_commands = self._load_commands(
            commands.get(f"{self.terminal_os.value}_commands", []), CommandType.TERMINAL
        ) if self.terminal else []
        self.spelling_commands = self._load_commands(commands.get("spelling_commands", []), CommandType.SPELLING)
        self.git_commands = self._load_commands(commands.get("git_commands", []), CommandType.GIT)
        self.interactive_commands = self._load_commands(commands.get("interactive_commands", []),
                                                        CommandType.INTERACTIVE)
        self.browser_commands = self._load_commands(commands.get("browser_commands", []), CommandType.BROWSER)

    @staticmethod
    def _load_commands(commands_list: list, command_type: CommandType) -> list:
        """Helper method to initialize commands from a given list."""
        return [
            CommandManager(cmd.get("name", ""), command_type, cmd.get("key", ""), cmd.get("num_key", ""))
            for cmd in commands_list
        ]

    def load_programming_commands(self) -> None:
        """
        Loads programming commands for the specified language from the commands file and sets the current language.
        """
        if not self.programming:
            return
        self.programming_commands = self._load_commands(self.commands[self.programming_language.value + "_commands"],
                                                        CommandType.PROGRAMMING)
        self.print_status()

    def load_terminal_commands(self) -> None:
        """
        Loads terminal commands for the specified operating system from the commands file and sets the current os.
        """
        if not self.terminal:
            return
        self.terminal_commands = self._load_commands(self.commands[self.terminal_os.value + "_commands"],
                                                     CommandType.TERMINAL)
        self.print_status()

    def handle_command(self, text: str) -> bool:
        """
        Processes a given text command by checking it against different command types.

        Parameters:
        - text (str): The command text to process.

        Returns:
        - bool: True if a command was successfully handled, False otherwise.
        """
        command_handlers = [
            self._handle_switch_commands,
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

    def _handle_command(self, text: str, command_list: list) -> bool:
        """
        Handles a command if the text matches any of the provided commands.

        Args:
          self: The object containing the necessary attributes.
          text: The command text to process.
          command_list: A list of command objects.

        Returns:
          bool: True if a command was handled, False otherwise.
        """
        for command in command_list:
            if text.startswith(command.name):
                if hasattr(command, 'command_executor'):
                    command.command_executor.execute(self)
                else:
                    command.execute(self)
                return True
        return False

    def _handle_switch_commands(self, text: str):
        return self._handle_command(text, self.switch_commands)

    def _handle_keyboard_command(self, text: str) -> bool:
        return self._handle_command(text, self.keyboard_commands)

    def _handle_git_command(self, text: str) -> bool:
        return self._handle_command(text, self.git_commands)

    def _handle_programming_command(self, text: str) -> bool:
        return self._handle_command(text, self.programming_commands)

    def _handle_terminal_command(self, text: str) -> bool:
        return self._handle_command(text, self.terminal_commands)

    def _handle_info_command(self, text: str) -> bool:
        return self._handle_command(text, self.info_commands)

    def _handle_selection_command(self, text: str) -> bool:
        return self._handle_command(text, self.selection_commands)

    def _handle_spelling_command(self, text: str) -> bool:
        return self._handle_command(text, self.spelling_commands)

    def _handle_interactive_command(self, text: str) -> bool:
        return self._handle_command(text, self.interactive_commands)

    def _handle_browser_command(self, text: str) -> bool:
        return self._handle_command(text, self.browser_commands)

    def print_status(self) -> None:
        """
        Prints the current status of typing activity, mode, terminal and programming language.
        """
        status = \
            f"Typing: {'started' if self.typing_active else 'stopped'}\n"\
            f"Mode: {self.mode.value}\n"\
            f"Programming: {'On' if self.programming else 'Off'} | {self.programming_language.value.capitalize()}\n"\
            f"Terminal: {'On' if self.terminal else 'Off'} | {self.terminal_os.value if self.terminal else ''}\n"\
            f"Punctuation: {'On' if self.punctuation else 'Off'} | Caps: {'On' if self.capitalize else 'Off'}\n"
        # Check if app_ui is available and update UI
        if self.app_ui:
            self.app_ui.update_status(status)
            self.app_ui.update_commands()
        else:
            print(status)

    def switch_mode(self) -> None:
        """Toggle between dictation and spelling modes."""
        self.mode = Mode.SPELLING if self.mode == Mode.DICTATION else Mode.DICTATION
        self.print_status()

    def switch_typing(self) -> None:
        """Toggle typing On/OFF."""
        self.typing_active = not self.typing_active
        self.print_status()

    def set_programming(self, state: bool) -> None:
        """Enable or disable programming mode."""
        self.programming = state

    def set_programming_language(self, language: ProgrammingLanguage):
        """Set the programming language."""
        self.programming_language = language

    def set_terminal_os(self, os: TerminalOS):
        """Set the terminal OS."""
        self.terminal_os = os

    @staticmethod
    def restart_script() -> None:
        """Restart the currently running script."""
        subprocess.Popen([sys.executable] + sys.argv)
        sys.exit()
