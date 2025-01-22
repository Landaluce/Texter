"""
This module defines the core functions for running a live speech-to-text interpreter
with command recognition and typing capabilities.

Key Features:
1. **Live Speech Interpretation**:
   - Continuously listens for speech input and processes it in real-time.
   - Uses a speech recognizer to convert spoken words into text.

2. **Command Handling**:
   - Identifies and executes predefined commands such as text formatting and application control.
   - Supports modes like dictation and spelling for text processing.

3. **Text Processing**:
   - Converts recognized text to specific cases (e.g., camel case, snake case).
   - Restores punctuation and capitalizes sentences based on application settings.

4. **Error Handling**:
   - Handles common errors during speech recognition (e.g., timeouts, unknown audio).
   - Processes special cases in recognized text to improve command recognition.

Functions:
- `run_live_speech_interpreter(app_state, app_ui, recognizer)`:
   Runs the live speech interpreter in a separate thread.

- `live_speech_interpreter(app_state, texter_ui, recognizer)`:
   Main loop for listening to and processing speech commands.

- `recognize_speech(recognizer, timeout)`:
   Captures and processes audio input using the given speech recognizer.

- `process_special_cases(text)`:
   Replaces specific phrases in the recognized text to handle common misinterpretations.

- `handle_spelling_mode(app_state, text)`:
   Processes text in spelling mode, converting input into a spelling-friendly format.

- `handle_dictation_mode(app_state, texter_ui, text)`:
   Processes text in dictation mode, supporting command recognition and formatting.

Dependencies:
- `threading`: For running the interpreter in a separate thread.
- `pyautogui`: For automating typing actions.
- `speech_recognition`: For converting speech to text.
- `src.commands.text_processor.TextProcessor`: For text processing tasks.
- `src.state.app_state.AppState`: Represents the application's current state.
- `src.ui.texter_ui.TexterUI`: UI integration for displaying recognized text and status updates.
- `src.utils.string_utils`: Utilities for text conversion (e.g., camel case, snake case).
- `src.utils.error_handler.noalsaerr`: Suppresses ALSA-related errors during microphone usage.

Usage:
    recognizer = sr.Recognizer()
    app_state = AppState()
    app_ui = TexterUI()
    run_live_speech_interpreter(app_state, app_ui, recognizer)
"""
from __future__ import annotations
import threading  # noqa: F401
from src.utils.gui_utils import write
import speech_recognition as sr
from src.commands.text_processor import TextProcessor
from src.utils.error_handler import noalsaerr
from src.state.app_state import AppState
from src.ui.texter_ui import TexterUI
from src.utils.string_utils import string_to_snake_case, string_to_camel_case, convert_to_spelling
from src.utils.constants import replacements


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

                texter_ui.append_text("You said:" + "~" + text + "~")

                handle_dictation_mode(app_state, texter_ui, text)
                handle_spelling_mode(app_state, text)

def recognize_speech(recognizer: sr.Recognizer, timeout: int = 2) -> str or None:
    """
    Recognizes and returns the speech from the given audio source using the specified recognizer.

    Parameters:
        recognizer (sr.Recognizer): The speech recognition object used to process the audio.
        timeout (int): Maximum number of seconds to wait for speech input before giving up.
                       If no speech is detected within this period, a WaitTimeoutError is raised.

    Returns:
        str: The recognized text, or None if recognition fails.
    """
    with sr.Microphone() as source:
        try:
            audio = recognizer.listen(source, timeout=timeout)
            text = recognizer.recognize_google(audio).lower()
            return text

        except sr.UnknownValueError:
            # print("Could not understand audio")
            pass
        except sr.RequestError as e:
            print(f"Error from Speech Recognition service: {e}")
            return None
        except sr.WaitTimeoutError:
            # Suppress timeout error message and continue
            pass
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None
    return None

def process_special_cases(text: str) -> str:
    """
    Handles special case replacements in recognized text.

    Args:
        text (str): The input text to process.

    Returns:
        str: The processed text with replacements applied.

    Raises:
        ValueError: If the input is not a string.
    """
    if not isinstance(text, str):
        raise ValueError(f"Expected 'txt' to be a string, but got {type(text)}")

    for target, replacement in replacements.items():
        text = text.replace(target, replacement)
    return text

def handle_spelling_mode(app_state, text: str) -> None:
    """
    Processes text in spelling mode by converting it to its spelled-out equivalent
    and applying necessary replacements.

    Args:
        app_state: The application's state, containing spelling-related configurations.
        text (str): The input text to be processed.
    """
    spelling_output = convert_to_spelling(text, app_state.spelling_commands)
    if spelling_output:
        write(spelling_output)

def handle_dictation_mode(app_state, texter_ui, text: str) -> None:
    """Processes text in dictation mode."""
    if text.startswith("camel case") or text.startswith("camelcase"):
        write(string_to_camel_case(text[len("camel case") + 1:]))
    elif text.startswith("small camel case"):
        write(string_to_camel_case(text[len("small camel case") + 1:], True))
    elif text.startswith("snake case"):
        write(string_to_snake_case(text[len("snake case") + 1:].strip()))
    elif text == "terminate texter":
        print("Terminating Texter...")
        app_state.terminate = True
        texter_ui.terminate_all_threads()
    elif not app_state.handle_command(text):
        if app_state.typing_active:
            if app_state.punctuation:
                text_processor = TextProcessor()
                text = text_processor.restore_punctuation(text)
                if app_state.capitalize:
                    text = text_processor.capitalize_sentences(text)
            write(text)
