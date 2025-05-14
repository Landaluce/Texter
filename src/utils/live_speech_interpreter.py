"""
This module contains the core logic for the live speech interpretation process.

It uses the speech_recognition library to capture audio from the microphone,
convert it to text, and then process the text to identify and handle commands
or perform dictation based on the application's current state.
"""
from __future__ import annotations
import speech_recognition as sr
import logging
from logging_config import setup_logging
from src.state.app_state import AppState
from src.ui.texter_ui import TexterUI
from src.utils.error_handler import noalsaerr
from src.utils.command_handler import handle_spelling_mode, handle_dictation_mode
from src.utils.speech_recognition import recognize_speech
from src.utils.special_case_processor import process_special_cases
setup_logging()

recognizer = sr.Recognizer()

def run_live_speech_interpreter(app_state: AppState, app_ui: TexterUI) -> None:
    """
    This function runs the live speech interpreter in a separate thread.
    """
    while not app_state.terminate:
        live_speech_interpreter(app_state, app_ui)


def live_speech_interpreter(app_state: AppState, texter_ui: TexterUI):
    """
    Continuously listens for and interprets speech commands, executing corresponding actions.

    This function uses a speech recognizer to convert spoken words into text and then processes
    the text to determine if it matches any predefined commands. If a command is recognized, it is
    executed; otherwise, the spoken text is typed out if typing mode is active.

    Parameters:
        texter_ui(TexterUI): frontend
        app_state (AppState): The current application state, including typing status and loaded commands.
    """
    with noalsaerr():
        while not app_state.terminate:
            text = recognize_speech(recognizer)
            if text:
                text = text.lower()
                text = process_special_cases(text)

                texter_ui.append_text(f"You said:~{text}~")
                logging.getLogger('general_logger').info(f"You said:~{text}~")

                handle_dictation_mode(app_state, texter_ui, text)
                handle_spelling_mode(app_state, text)
