"""
Module that defines classes for executing various types of commands in a GUI.
The classes support programming, keyboard, terminal, selection, switch, and interactive commands.

Each command executor corresponds to a specific action, such as typing programming commands (Python/Java),
executing terminal commands, simulating keyboard actions, switching app states, or interacting with the browser.
The primary function of each class is to simulate user interactions within a graphical interface.

Classes:
    - ProgrammingCommandExecutor: Executes programming commands for Python and Java.
    - KeyboardCommandExecutor: Executes keyboard-related commands such as hotkeys and key presses.
    - SwitchCommandExecutor: Executes commands to switch application states (e.g., programming mode, terminal mode).
    - InfoCommandExecutor: Executes info commands that simply type text into the GUI.
    - GitCommandExecutor: Executes Git-related commands within the terminal or GUI.
    - TerminalCommandExecutor: Executes terminal-related commands such as navigating directories or system commands.
    - SelectionCommandExecutor: Executes commands to manipulate selected text (e.g., copy, paste, delete).
    - InteractiveCommandExecutor: Executes interactive commands, including fetching and reading out the time or date.
    - BrowserCommandExecutor: Executes browser-related commands such as switching tabs, opening windows, and navigating pages.

Each executor is initialized with a command key or name and can be invoked to simulate a GUI interaction.
"""
from src.utils.gui_utils import press, write
from src.constants.command_constants import (TerminalOS, simple_terminal_command_names)
from src.utils.text_to_speech import text_to_speech
from src.utils.date_time_utils import (get_current_time, get_current_date, month_number_to_name, day_number_to_name,
                                       get_day_of_week)
import logging
from logging_config import setup_logging

setup_logging()
warning_logger = logging.getLogger('warning_logger')
error_logger = logging.getLogger('error_logger')


class ActionExecutor:
    """
    A class responsible for executing predefined actions or operations.
    """
    def __init__(self):
        pass

    @staticmethod
    def execute(action: str, app_state=None):
        """
        Executes predefined actions or operations.
        """
        exec(action)
        if app_state:
            app_state.update_status()


class TerminalCommandExecutor:
    """
    A class that executes selection commands within a GUI.
    """

    def __init__(self, key: str, name: str):
        """
        Initializes a `TerminalCommandExecutor` instance.

        Args:
            name (str): The name of the selection command to be executed.
        """
        self.key = key
        self.name = name

    def execute(self, app_state) -> None:
        """
        Executes a terminal command.

        Args:
            app_state (AppState): The current application state, including information about the terminal OS.
        """
        if ((self.name.startswith("change permissions") and app_state.terminal_os == TerminalOS.LINUX) or
                self.name.startswith("go to")):
            write(self.key)
        elif self.name in simple_terminal_command_names:
            write(self.key)
            press("enter")
        else:
            pass


class InteractiveCommandExecutor:
    """
    A class that executes text to speech commands.
    """

    def __init__(self, name: str):
        """
        Initializes a `SelectionCommandExecutor` instance.

        Args:
            name (str): The name of the selection command to be executed.
        """
        self.name = name

    def execute(self) -> None:
        """
        Executes the interactive command.
        """
        if self.name.startswith(("what time is it", "what's the time")):
            current_time = get_current_time()
            text_to_speech(f"it's {current_time}")

        elif self.name.startswith("what's the date"):
            current_date_time = get_current_date()
            month, day = current_date_time.strftime("%m-%d").split("-")
            month_name = month_number_to_name(int(month))
            day_name = day_number_to_name(int(day))

            week_day = get_day_of_week(current_date_time.strftime("%Y-%m-%d"))
            current_date = f"{week_day}, {month_name} {day_name}"
            text_to_speech(current_date)

        else:
            text_to_speech("no input")
