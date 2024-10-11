# Standard library imports
from __future__ import annotations
import threading
import json

# Third-party imports
import pyautogui as gui
import speech_recognition as sr

# Local application imports
from PunctuationModel import PunctuationModel
# from TextProcessor import TextProcessor
from src.ErrorHandler import noalsaerr
from src.AppState import AppState
from src.TexterUI import TexterUI

# text_processor = TextProcessor()
punctuation_model = PunctuationModel()


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
        except sr.WaitTimeoutError:
            # Suppress timeout error message and continue
            pass
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
    return None


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
            # with sr.Microphone():
            app_state.print_status()
            texter_ui.print_status()
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
                    texter_ui.append_text(f"Switched to {app_state.mode} mode.")
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
                # Handle spelling mode
                if app_state.mode == "spelling":
                    spelling_output = convert_to_spelling(text, app_state.spelling_commands)
                    if spelling_output:
                        gui.typewrite(spelling_output)
                    else:
                        texter_ui.append_text("No valid spelling commands found.")
                    continue

                # Handle dictation mode
                if app_state.mode == "dictation":
                    if text.startswith("type"):
                        if app_state.typing_active:
                            gui.typewrite(text[5:])
                    else:
                        # Check if termination is requested
                        if text == "terminate texter":
                            print("Terminating Texter...")
                            app_state.terminate = True
                            texter_ui.terminate_all_threads()
                            break  # Exit the loop to stop the thread
                        if not app_state.handle_command(text):
                            if app_state.typing_active:
                                if app_state.punctuation:
                                    text = punctuation_model.restore_punctuation(text)
                                    if app_state.capitalize:
                                        text = punctuation_model.capitalize_sentences(text)
                                gui.write(text)


def convert_to_spelling(text: str, spelling_commands: list) -> str:
    """
    Convert spoken words to corresponding spelling characters.

    Parameters:
        text (str): The command text to process.
        spelling_commands (dict): spelling commands
    Returns:
        eg:
            input text: alpha beta
            output: ab
    """
    words = text.split()
    output = []
    for word in words:
        for command in spelling_commands:
            if command.name == word:
                output.append(command.key)
                break
    return ''.join(output)
