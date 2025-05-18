"""
This module contains the core logic for the live speech interpretation process.

It uses the speech_recognition library to capture audio from the microphone,
convert it to text, and then process the text to identify and handle commands
or perform dictation based on the application's current state.
"""
from __future__ import annotations
import time
import speech_recognition as sr
from src.utils.logging_utils import info_logger, error_logger
from src.state.app_state import AppState
from src.ui.texter_ui import TexterUI
from src.utils.error_handler import noalsaerr
from src.utils.command_handler import handle_spelling_mode, handle_dictation_mode
from src.utils.speech_recognition import recognize_speech
from src.utils.special_case_processor import process_special_cases

recognizer = sr.Recognizer()

def run_live_speech_interpreter(app_state: AppState, app_ui: TexterUI) -> None:
    """
    Runs the live speech interpreter in a separate thread.

    Args:
        app_state (AppState): The current application state.
        app_ui (TexterUI): The UI instance.

    This function will loop until app_state.terminate is set to True.
    """
    while not app_state.terminate:
        try:
            live_speech_interpreter(app_state, app_ui)
        except Exception as e:
            info_logger.error(f"Error in live speech interpreter: {e}", exc_info=True)
            time.sleep(1)  # Prevent tight error loop


def live_speech_interpreter(app_state: AppState, texter_ui: TexterUI):
    """
    Continuously listens for and interprets speech commands, executing corresponding actions.

    Args:
        texter_ui(TexterUI): frontend
        app_state (AppState): The current application state, including typing status and loaded commands.
    
    This function will loop until app_state.terminate is set to True.
    """
    with noalsaerr():
        while not app_state.terminate:
            try:
                text = recognize_speech(recognizer)
                if text:
                    text = text.lower()
                    text = process_special_cases(text)

                    texter_ui.append_text(f"You said:~{text}~")
                    info_logger.info(f"You said:~{text}~")

                    handle_dictation_mode(app_state, texter_ui, text)
                    handle_spelling_mode(app_state, text)
            except Exception as e:
                error_logger.error(f"Error in live speech interpreter: {e}", exc_info=True)
                time.sleep(5)  # Prevent tight error loop
