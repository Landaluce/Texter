"""
Main function that initializes the application state and starts the live speech interpreter.

This function sets up the application by performing the following tasks:
- Creates an instance of AppState and initializes the UI.
- Loads the necessary commands using the get_commands function.
- Sets up the speech recognizer using the speech_recognition library.
- Starts the live speech interpretation process in a separate thread to handle speech commands in real-time.

Example Usage:
    Run the script to initialize the application, load commands, and start live speech recognition.

Raises:
    RuntimeError: If the commands cannot be loaded or if the speech interpreter thread fails to start.
"""
import threading  # noqa: F401
import logging
from logging_config import setup_logging
from src.utils.main_utils import initialize_application, start_speech_interpreter

setup_logging()
warning_logger = logging.getLogger('warning_logger')
error_logger = logging.getLogger('error_logger')
info_logger = logging.getLogger('general_logger')


def main():
    """
    Initializes the application app_state and starts the live speech interpreter.
    This function sets up the application by:
    - Creating an instance of AppState
    - Loading the necessary commands.
    - Initializing the speech recognizer.
    - Starting the live speech interpretation process in a separate thread.

    Example Usage:
        Run the script to start the application and speech recognition.

    Raises:
        RuntimeError: If commands cannot be loaded or threads fail to start.
    """
    try:
        app, app_state, recognizer, commands = initialize_application()
        start_speech_interpreter(app_state, app, recognizer)

        # Initialize UI
        info_logger.info("Starting UI...")
        app.init_ui(app_state, commands)

    except Exception as e:
        error_logger.error(f"Application startup failed: {e}", exc_info=True)


if __name__ == "__main__":
    main()