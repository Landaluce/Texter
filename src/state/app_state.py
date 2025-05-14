"""
This module defines the `AppState` class, which encapsulates the state and behavior
of an application supporting multiple modes, commands, and configurations.

The `AppState` class manages:
- Typing and application modes (e.g., dictation, spelling).
- Commands for various functionalities, including keyboard, terminal, programming, and more.
- Configurations for programming languages and terminal operating systems.
- Application settings such as punctuation, capitalization, and spelling.

Features:
1. Command Management:
   - Dynamically loads commands based on configurations.
   - Handles and executes commands across different categories (e.g., terminal, programming).
2. Mode and State Management:
   - Switches between dictation and spelling modes.
   - Toggles features like punctuation, capitalization, and typing activity.
3. Programming and Terminal Support:
   - Supports different programming languages for contextual commands.
   - Adapts terminal commands based on the operating system.
4. Status Reporting:
   - Generates and updates status strings reflecting the current application state.
   - Integrates with a UI or prints to the console when the UI is unavailable.
5. Script Management:
   - Allows the script to restart itself programmatically.

Dependencies:
- `sys`: For accessing system-specific parameters and functions.
- `subprocess`: For restarting the application script.
- `src.commands.command_manager.CommandManager`: For managing individual commands.
- `src.utils.constants`: For enumerations like `CommandType`, `ProgrammingLanguage`, `TerminalOS`, and `Mode`.

Usage:
    app_state = AppState()
    app_state.load_commands(commands_config)
    app_state.switch_typing()
    app_state.handle_command("example_command")

Classes:
- `AppState`: Represents the core state and functionality of the application.
"""
import sys
import subprocess
from typing import List

from src.commands.command_manager import CommandManager
from src.constants.command_constants import CommandType, ProgrammingLanguage, TerminalOS
from src.constants.app_state_constants import command_groups, Mode


class AppState:
    """
    represents the state of the application, including typing status,
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

        # Command groups
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
        # Dynamically load common commands
        for group, command_type in command_groups.items():
            try:
                setattr(self, group, self._load_commands(commands.get(group, []), command_type))
            except Exception as e:
                print(f"could not load {group} commands")
                print(e)

        # Load programming commands (if applicable)
        self.programming_commands = (
            self._load_commands(commands.get(f"{self.programming_language.value}_commands", []),
                                CommandType.PROGRAMMING)
            if self.programming else []
        )

        # Load terminal commands (if applicable)
        self.terminal_commands = (
            self._load_commands(commands.get(f"{self.terminal_os.value}_commands", []), CommandType.TERMINAL)
            if self.terminal else []
        )

    @staticmethod
    def _load_commands(commands_list: list, command_type: CommandType) -> list:
        """Helper method to initialize commands from a given list."""
        return [
            CommandManager(cmd.get("name", ""), command_type, cmd.get("key", ""), cmd.get("num_key", ""),
                           cmd.get("action", ""))
            for cmd in commands_list
        ]

    def load_programming_commands(self) -> None:
        """
        Loads programming commands for the specified language from the commands file and sets the current language.
        """
        if not self.programming:
            print("Warning: Cannot load programming commands, commands configuration not loaded.")
            return
        self.programming_commands = self._load_commands(self.commands[self.programming_language.value + "_commands"],
                                                        CommandType.PROGRAMMING)
        self.update_status()

    def load_terminal_commands(self) -> None:
        """
        Loads terminal commands for the specified operating system from the command file and sets the current os.
        """
        if not self.terminal:
            print("Warning: Cannot load terminal commands, commands configuration not loaded.")
            return
        self.terminal_commands = self._load_commands(self.commands[self.terminal_os.value + "_commands"],
                                                     CommandType.TERMINAL)
        self.update_status()

    def get_all_commands(self) -> List[CommandManager]:
        """
        Compiles a single list of all currently loaded CommandManager objects from all groups.

        Returns:
            A list of all CommandManager objects.
        """
        return (
                self.switch_commands +
                self.keyboard_commands +
                self.info_commands +
                self.selection_commands +
                self.programming_commands +
                self.terminal_commands +
                self.spelling_commands +
                self.git_commands +
                self.interactive_commands +
                self.browser_commands
        )

    def handle_command(self, text: str) -> bool:
        """
        Processes a given text command by checking it against all loaded commands.

        Parameters:
        - text (str): The command text to process.

        Returns:
        - bool: True if a command was successfully handled, False otherwise.
        """
        all_commands = self.get_all_commands()

        for command in all_commands:
            if text.startswith(command.name):
                try:
                    if hasattr(command, 'command_executor'):
                        command.command_executor.execute(self)
                    else:
                        command.execute(self)
                    return True
                except Exception as e:
                    print(f"Error executing command '{command.name}': {e}")
                    # TODO: update UI with an error message
                    return False
        return False

    def update_status(self) -> None:
        """Updates the UI with the current status or prints it to the console."""
        status = self.generate_status()
        self._update_ui_state(status)

    def generate_status(self) -> str:
        """
        Generates the current status string.

        Returns:
        str: A formatted string showing the current state
        """
        return (f"Typing: {'Started' if self.typing_active else 'Stopped'}\n"
                f"Mode: {self.mode.value.capitalize()}\n"
                f"Programming: {'On' if self.programming else 'Off'} | "
                f"{self.programming_language.value.capitalize()}\n"
                f"Terminal: {'On' if self.terminal else 'Off'} | "
                f"{self.terminal_os.value.capitalize()}\n"
                f"Punctuation: {'On' if self.punctuation else 'Off'} | "
                f"Caps: {'On' if self.capitalize else 'Off'}"
        )

    def _update_ui_state(self, status: str) -> None:
        """Updates the UI state or prints the status to the console if no UI is available."""
        if self.app_ui:
            self.app_ui.update_status(status)
            self.app_ui.update_commands()
        else:
            print(status)

    def switch_mode(self) -> None:
        """Toggle between dictation and spelling modes."""
        self.mode = Mode.SPELLING if self.mode == Mode.DICTATION else Mode.DICTATION
        self.update_status()

    def switch_typing(self) -> None:
        """Toggle typing On/OFF."""
        self.switch_attribute("typing_active")
        self.update_status()

    def switch_punctuation(self) -> None:
        """Toggle punctuation On/OFF."""
        self.switch_attribute("punctuation")
        self.punctuation = self.capitalize or self.punctuation
        self.update_status()

    def switch_capitalization(self) -> None:
        """Toggle capitalization On/OFF."""
        self.switch_attribute("capitalize")
        self.capitalize = self.punctuation or self.capitalize
        self.update_status()

    def switch_attribute(self, attribute):
        """Toggle the boolean value of a given attribute."""
        if hasattr(self, attribute):
            current_value = getattr(self, attribute)
            if isinstance(current_value, bool):
                setattr(self, attribute, not current_value)
            else:
                print(f"Warning: Attribute '{attribute}' is not a boolean, cannot toggle.")
        else:
             print(f"Warning: Attribute '{attribute}' not found.")

    def set_programming_language(self, language: ProgrammingLanguage) -> None:
        """Set the programming language."""
        self.programming_language = language

    def set_terminal_os(self, os: TerminalOS) -> None:
        """Set the terminal OS."""
        self.terminal_os = os

    @staticmethod
    def restart_script() -> None:
        """Restart the currently running script."""
        subprocess.Popen([sys.executable] + sys.argv)
        sys.exit()
