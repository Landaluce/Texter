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
- `src.commands.command_executors`: Contains the specific command executors for each command type (e.g.,
    `KeyboardCommandExecutor`, `ProgrammingCommandExecutor`).
- `src.utils.constants`: Contains the `CommandType` enum, which classifies commands into various categories.

Usage:
    command = CommandManager(name="Type Hello", command_type=CommandType.KEYBOARD, key="h")
    command.execute(app_state)
    command_dict = command.commands_to_dict(include_num_key=False)
"""
from src.commands.command_executors import (TerminalCommandExecutor, InteractiveCommandExecutor, ActionExecutor)
from src.constants.command_constants import CommandType
import logging
from logging_config import setup_logging

setup_logging()
error_logger = logging.getLogger('error_logger')


class CommandManager:
    """
    Represents a command that can be executed based on recognized speech input.
    """

    def __init__(self, name: str, command_type: CommandType, key=None, num_key=None, action=None):
        """
        initializes a new Command instance.

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
        self.action = action

        self.action_executor = ActionExecutor()
        self.terminal_command_executor = TerminalCommandExecutor(self.key, self.name)
        self.interactive_command_executor = InteractiveCommandExecutor(self.name)

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
    Executes the command according to its type using the current application state.

    Args:
        app_state (AppState): The current application state.

    Depending on the command type, delegates execution to the appropriate executor (action, terminal, or interactive).
    """
        if self.command_type == CommandType.SWITCH:
            self.action_executor.execute(self.action, app_state)

        elif self.command_type == CommandType.TERMINAL:
            self.terminal_command_executor.execute(app_state)

        elif self.command_type == CommandType.INTERACTIVE:
            self.interactive_command_executor.execute()

        else:
            print("in command manager.execute ELSE", self.command_type, self.action)
            self.action_executor.execute(self.action)

