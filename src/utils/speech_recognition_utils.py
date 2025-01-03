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
            text = recognize_speech(recognizer)  # , source)
            if text:
                # Hardcoded check to always output "Texter"
                text = text.lower()
                if "dexter" in text:
                    text = text.replace("dexter", "texter")
                if "texture" in text:
                    text = text.replace("texture", "texter")

                if text.endswith("lift"):
                    text = text.replace("lift", "left")
                if text.endswith("wright"):
                    text = text.replace("wright", "right")

                texter_ui.append_text("You said:" + "~" + text + "~")

                if text == "switch mode":
                    app_state.switch_mode()
                    # texter_ui.append_text(f"Switched to {app_state.mode} mode.")
                    continue  # Skip further processing after switching modes
                if text == "switch punctuation":
                    app_state.punctuation = not app_state.punctuation
                    if not app_state.punctuation:
                        app_state.capitalize = False
                    app_state.print_status()
                    continue
                if text == "switch caps":
                    app_state.punctuation = not app_state.capitalize
                    app_state.capitalize = not app_state.capitalize
                    app_state.print_status()
                    continue

                # Handle spelling
                # TODO: fix to enable termination and maybe other commands in spelling mode
                if app_state.mode == Mode.SPELLING:
                    spelling_output = convert_to_spelling(
                        text, app_state.spelling_commands
                    )
                    if spelling_output:
                        gui.typewrite(spelling_output)
                    else:
                        texter_ui.append_text("No valid spelling commands found.")
                    continue

                # Handle dictation mode
                if app_state.mode == Mode.DICTATION:
                    if text.startswith("type"):
                        if app_state.typing_active:
                            gui.typewrite(text[5:])
                    else:
                        if text.startswith("camel case"):
                            gui.write(
                                string_to_camel_case(text[len("camel case") + 1 :])
                            )
                            continue
                        if text.startswith("camelcase"):
                            gui.write(
                                string_to_camel_case(text[len("camelcase") + 1 :])
                            )
                            continue
                        if text.startswith("small camel case"):
                            gui.write(
                                string_to_camel_case(
                                    text[len("small camel case") + 1 :], True
                                )
                            )
                            continue
                        if text.startswith("small camelcase"):
                            gui.write(
                                string_to_camel_case(
                                    text[len("small camelcase") + 1 :], True
                                )
                            )
                            continue
                        if text.startswith("snake case"):
                            gui.write(
                                string_to_snake_case(
                                    text[len("snake case") + 1 :].strip()
                                )
                            )
                            continue

                        # Check if termination is requested
                        if text == "terminate texter":
                            print("Terminating Texter...")
                            app_state.terminate = True
                            texter_ui.terminate_all_threads()
                            break  # Exit the loop to stop the thread

                        if not app_state.handle_command(text):
                            if app_state.typing_active:
                                if app_state.punctuation:
                                    text = text_processor.restore_punctuation(text)
                                    if app_state.capitalize:
                                        text = text_processor.capitalize_sentences(text)
                                gui.write(text)


def run_live_speech_interpreter(
    app_state: AppState, app_ui: TexterUI, recognizer
) -> None:
    """
    This function runs the live speech interpreter in a separate thread.
    """
    while not app_state.terminate:
        live_speech_interpreter(app_state, app_ui, recognizer)
