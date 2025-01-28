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


def run_live_speech_interpreter(app_state: AppState, app_ui: TexterUI, recognizer) -> None:
    """
    This function runs the live speech interpreter in a separate thread.
    """
    while not app_state.terminate:
        live_speech_interpreter(app_state, app_ui, recognizer)


def live_speech_interpreter(app_state: AppState, texter_ui: TexterUI, recognizer: sr.Recognizer):
    """
    Continuously listens for and interprets speech commands, executing corresponding actions.

    This function utilizes a speech recognizer to convert spoken words into text and then processes
    the text to determine if it matches any predefined commands. If a command is recognized, it is
    executed; otherwise, the spoken text is typed out if typing mode is active.

    Parameters:
        texter_ui(TexterUI): frontend
        app_state (AppState): The current application state, including typing status and loaded commands.
        recognizer (sr.Recognizer): The speech recognition object used to process the audio input.
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
