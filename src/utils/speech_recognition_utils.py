from __future__ import annotations
import threading  # noqa: F401
import pyautogui as gui
import speech_recognition as sr
from src.commands.text_processor import TextProcessor
from src.utils.error_handler import noalsaerr
from src.state.app_state import AppState
from src.ui.texter_ui import TexterUI
from src.utils.string_utils import string_to_snake_case, string_to_camel_case, convert_to_spelling
from src.utils.constants import Mode

text_processor = TextProcessor()


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
    """Handles special case replacements in recognized text."""
    if not isinstance(text, str):
        raise ValueError(f"Expected 'txt' to be a string, but got {type(text)}")
    replacements = {
        "dexter": "texter",
        "texture": "texter",
        "lift": "left",
        "wright": "right",
    }
    for target, replacement in replacements.items():
        text = text.replace(target, replacement)
    return text

def handle_switch_commands(app_state, command: str) -> bool:
    """Handles switching app state commands."""
    if command == "switch mode":
        app_state.switch_mode()
        return True
    if command == "switch punctuation":
        app_state.punctuation = not app_state.punctuation
        if not app_state.punctuation:
            app_state.capitalize = False
        app_state.update_status()
        return True
    if command == "switch caps":
        app_state.capitalize = not app_state.capitalize
        app_state.update_status()
        return True
    return False

def handle_spelling_mode(app_state, texter_ui, text: str):
    """Processes text in spelling mode."""
    spelling_output = convert_to_spelling(text, app_state.spelling_commands)
    if spelling_output:
        gui.typewrite(spelling_output)
    else:
        texter_ui.append_text("No valid spelling commands found.")

def handle_dictation_mode(app_state, texter_ui, text: str):
    """Processes text in dictation mode."""
    if text.startswith("type") and app_state.typing_active:
        gui.typewrite(text[5:])
    elif text.startswith("camel case"):
        gui.write(string_to_camel_case(text[len("camel case") + 1:]))
    elif text.startswith("small camel case"):
        gui.write(string_to_camel_case(text[len("small camel case") + 1:], True))
    elif text.startswith("snake case"):
        gui.write(string_to_snake_case(text[len("snake case") + 1:].strip()))
    elif text == "terminate texter":
        print("Terminating Texter...")
        app_state.terminate = True
        texter_ui.terminate_all_threads()
    elif not app_state.handle_command(text):
        if app_state.typing_active:
            if app_state.punctuation:
                text = text_processor.restore_punctuation(text)
                if app_state.capitalize:
                    text = text_processor.capitalize_sentences(text)
            gui.write(text)


def live_speech_interpreter(
        app_state: AppState, texter_ui: TexterUI, recognizer: sr.Recognizer
):
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

                handle_switch_commands(app_state, text)
                handle_spelling_mode(app_state, texter_ui, text)
                handle_dictation_mode(app_state, texter_ui, text)


def run_live_speech_interpreter(app_state: AppState, app_ui: TexterUI, recognizer) -> None:
    """
    This function runs the live speech interpreter in a separate thread.
    """
    while not app_state.terminate:
        live_speech_interpreter(app_state, app_ui, recognizer)
