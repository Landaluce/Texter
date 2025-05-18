"""
Main entry point for the Texter application.

This script initializes logging, loads command definitions, sets up the application state and UI,
and starts the live speech interpreter in a separate thread. It handles errors during initialization
and ensures that the application is ready to process speech commands in real-time.

Example:
    Run this script directly to launch the Texter application.

Raises:
    RuntimeError: If command files cannot be loaded or if initialization fails.
"""
import json
import threading  # noqa: F401
import logging

from logging_config import setup_logging
from src.constants.main_constants import command_files_directory
from src.state.app_state import AppState
from src.ui.texter_ui import TexterUI
from src.utils.command_utils import get_commands
from src.utils.live_speech_interpreter import run_live_speech_interpreter

setup_logging()
warning_logger = logging.getLogger('warning_logger')
error_logger = logging.getLogger('error_logger')
info_logger = logging.getLogger('general_logger')


def initialize_application():
    """Initializes the application state, loads commands, and sets up UI."""
    app = TexterUI(command_files_directory)
    app_state = AppState(app)

    try:
        commands = get_commands(command_files_directory)
        app_state.load_commands(commands)
        info_logger.info(f"Loaded {len(commands)} commands successfully.")
    except FileNotFoundError:
        error_logger.error(f"Command file directory not found: {command_files_directory}", exc_info=True)
        raise RuntimeError("Command directory not found.")
    except json.JSONDecodeError:
        error_logger.error("Failed to parse command files (invalid JSON).", exc_info=True)
        raise RuntimeError("Failed to parse command files.")
    except Exception as e:
        error_logger.error(f"An unexpected error occurred while loading commands: {e}", exc_info=True)
        raise RuntimeError("An unexpected error occurred during command loading.") from e

    start_speech_interpreter(app_state, app)

    return app, app_state, commands


def start_speech_interpreter(app_state, app):
    """Starts the live speech interpreter in a separate thread."""
    speech_thread = threading.Thread(
        target=run_live_speech_interpreter, args=(app_state, app), daemon=True
    )
    speech_thread.start()
    app.speech_thread = speech_thread


def main():
    """
    Initializes and runs the application.
    """
    try:
        app, app_state, commands = initialize_application()
        info_logger.info("Starting UI...")
        app.init_ui(app_state, commands)
    except RuntimeError as e:
        error_logger.critical(f"Application failed to initialize: {e}")
    except Exception as e:
        error_logger.critical(f"An unhandled error occurred during application execution: {e}", exc_info=True)


if __name__ == "__main__":
    main()
