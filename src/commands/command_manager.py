"""
This module defines the CommandManager class, which handles the execution of various commands
based on recognized speech input. Commands can be of different types such as keyboard, programming,
switch, terminal, and more. The CommandManager initializes the appropriate command executors
and provides methods for executing and converting commands to a dictionary representation.

Key Features:
1. **Command Execution**:
   - Executes different command types using specific executors for each command type.
   - Supports various commands like keyboard input, programming actions, terminal commands, and more.

2. **Command Representation**:
   - Converts command objects into dictionaries for easy storage or transmission.

Classes:
- `CommandManager`:
   Manages different command types and their corresponding executors. It also provides methods
   for executing commands and converting them into a dictionary format.

Methods:
- `__init__(self, name: str, command_type: CommandType, key=None, num_key=None)`:
   Initializes a new command instance with the given name, command type, key, and optional num_key.

- `commands_to_dict(self, include_num_key: bool=True) -> dict`:
   Converts the current command object into a dictionary format.

- `execute(self, app_state)`:
   Executes the appropriate command based on the command type. It interacts with the application state
   to perform the desired action (e.g., typing, switching modes, terminal commands, etc.).

Dependencies:
- `src.commands.command_executors`: Contains the specific command executors for each command type (e.g., `KeyboardCommandExecutor`, `ProgrammingCommandExecutor`).
- `src.utils.constants`: Contains the `CommandType` enum, which classifies commands into various categories.

Usage:
    command = CommandManager(name="Type Hello", command_type=CommandType.KEYBOARD, key="h")
    command.execute(app_state)
    command_dict = command.commands_to_dict(include_num_key=False)
"""

from src.commands.command_executors import (ProgrammingCommandExecutor, KeyboardCommandExecutor, SwitchCommandExecutor,
                                            InfoCommandExecutor, GitCommandExecutor, TerminalCommandExecutor,
                                            SelectionCommandExecutor, InteractiveCommandExecutor,
                                            BrowserCommandExecutor)
from src.utils.constants import CommandType


class CommandManager:
    """
    Represents a command that can be executed based on recognized speech input.
    """

    def __init__(self, name: str, command_type: CommandType, key=None, num_key=None):
        """
        Initializes a new Command instance.

        Args:
            name (str): The name of the command.
            command_type (CommandType): The type of command (e.g., KEYBOARD, SWITCH).
            key (str, optional): The key to be pressed for keyboard or programming commands.
            num_key (str, optional): The key used for commands that can be repeated multiple times.
        """
        self.name = name
        self.command_type = command_type
        self.key = key
        self.num_key = num_key

        self.programming_command_executor = ProgrammingCommandExecutor(self.key)
        self.keyboard_command_executor = KeyboardCommandExecutor(self.key, self.name, self.num_key)
        self.switch_command_executor = SwitchCommandExecutor(self.name)
        self.info_command_executor = InfoCommandExecutor(self.key)
        self.git_command_executor = GitCommandExecutor(self.key)
        self.terminal_command_executor = TerminalCommandExecutor(self.key, self.name)
        self.selection_command_executor = SelectionCommandExecutor(self.name)
        self.interactive_command_executor = InteractiveCommandExecutor(self.name)
        self.browser_command_executor = BrowserCommandExecutor(self.name)

    def commands_to_dict(self, include_num_key: bool=True) -> dict:
        """
        Converts the current command object into a dictionary representation.

        Args:
          include_num_key (bool, optional): A flag indicating whether to include the "num_key" in the output dictionary.

        Returns:
          dict: A dictionary representation of the command object.
        """
        command_dict = {
            "name": self.name,
            "command_type": self.command_type.name,
            "key": self.key,
        }
        if include_num_key:
            command_dict["num_key"] = self.num_key
        return command_dict

    def execute(self, app_state) -> None:
        """
        Executes the command based on its type.

        Parameters:
            app_state (AppState): The current application state.

        Depending on the command type, this method will either execute a keyboard command,
        toggle typing activity, type out a programming or info command, or execute a selection command.
        """
        if self.command_type == CommandType.KEYBOARD:
            self.keyboard_command_executor.execute()

        elif self.command_type == CommandType.SWITCH:
            self.switch_command_executor.execute(app_state)

        elif self.command_type == CommandType.INFO:
            self.info_command_executor.execute()

        elif self.command_type == CommandType.PROGRAMMING:
            self.programming_command_executor.execute(app_state)

        elif self.command_type == CommandType.TERMINAL:
            self.terminal_command_executor.execute(app_state)

        elif self.command_type == CommandType.SELECTION:
            self.selection_command_executor.execute()

        elif self.command_type == CommandType.GIT:
            self.git_command_executor.execute()

        elif self.command_type == CommandType.INTERACTIVE:
            self.interactive_command_executor.execute()

        elif self.command_type == CommandType.BROWSER:
            self.browser_command_executor.execute()
