"""
Command Executors Module

This module defines classes for executing various types of commands within the Texter application.

Classes:
    ActionExecutor:
        Executes predefined actions or operations, typically by evaluating a string of Python code.
        Optionally updates the application state after execution.

    InteractiveCommandExecutor:
        Executes interactive commands, such as responding to user queries about the current time or date
        using text-to-speech. Initialized with a command name and provides logic to handle specific
        interactive requests.

Usage:
    Use ActionExecutor for direct action execution, and InteractiveCommandExecutor for commands
    that require user interaction or dynamic responses.
"""
from src.utils.gui_utils import press, write # DO NOT REMOVE
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
