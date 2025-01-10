from src.commands.command_executors import (ProgrammingCommandExecutor, KeyboardCommandExecutor, SwitchCommandExecutor,
                                            InfoCommandExecutor, GitCommandExecutor, TerminalCommandExecutor,
                                            SelectionCommandExecutor, InteractiveCommandExecutor,
                                            BrowserCommandExecutor)
from src.utils.constants import CommandType


class CommandManager:
    """
    Represents a command that can be executed based on recognized speech input.

    Attributes:
        name (str): The name of the command.
        command_type (CommandType): The type of command (e.g., KEYBOARD, SWITCH).
        key (str, optional): The key to be pressed for keyboard or programming commands.
        num_key (str, optional): The key used for commands that can be repeated multiple times.
    """

    def __init__(self, name: str, command_type: CommandType, key=None, num_key=None):
        """
        Initializes a new Command instance.
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
