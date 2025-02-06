import threading

import speech_recognition as sr

from src.constants.main_constants import command_files_directory
from src.main import info_logger, error_logger
from src.state.app_state import AppState
from src.ui.texter_ui import TexterUI
from src.utils.command_utils import get_commands
from src.utils.live_speech_interpreter import run_live_speech_interpreter


def initialize_application():
    """Initializes the application state, loads commands, and sets up UI."""
    app = TexterUI(command_files_directory)
    recognizer = sr.Recognizer()
    app_state = AppState(app)

    try:
        commands = get_commands(command_files_directory)
        app_state.load_commands(commands)
        info_logger.info(f"Loaded {len(commands)} commands successfully.")
    except Exception as e:
        error_logger.info(f"Failed to load commands: {e}")
        raise RuntimeError("Command loading failed.") from e

    return app, app_state, recognizer, commands


def start_speech_interpreter(app_state, app, recognizer):
    """Starts the live speech interpreter in a separate thread."""
    speech_thread = threading.Thread(
        target=run_live_speech_interpreter, args=(app_state, app, recognizer), daemon=True
    )
    speech_thread.start()
    app.speech_thread = speech_thread
