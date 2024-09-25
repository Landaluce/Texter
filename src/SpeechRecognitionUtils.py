# Standard library imports
import json

# Third-party imports
import pyautogui as gui
import speech_recognition as sr

# Local application imports
from src.ErrorHandler import noalsaerr


def recognize_speech(recognizer, source):
    """
    Recognizes and returns the speech from the given audio source using the specified recognizer.

    Parameters:
        recognizer (sr.Recognizer): The speech recognition object used to process the audio.
        source (sr.Microphone): The audio source from which to listen for speech.

    Returns:
        str: The recognized text, or None if recognition fails.
    """
    try:
        audio = recognizer.listen(source, timeout=2)
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

def live_speech_interpreter(state, texter_ui, keyboard_commands, info_commands, selection_commands, recognizer):
    """
    Continuously listens for and interprets speech commands, executing corresponding actions.

    This function utilizes a speech recognizer to convert spoken words into text and then processes
    the text to determine if it matches any predefined commands. If a command is recognized, it is
    executed; otherwise, the spoken text is typed out if typing mode is active.

    Parameters:
        texter_ui(TexterUI): frontend
        state (AppState): The current application state, including typing status and loaded commands.
        keyboard_commands (list): A list of keyboard commands to check against the recognized text.
        info_commands (list): A list of info commands to check against the recognized text.
        selection_commands (list): A list of selection commands to check against the recognized text.
        recognizer (sr.Recognizer): The speech recognition object used to process the audio input.
    """
    with noalsaerr():
        with sr.Microphone() as source:
            state.print_status()
            texter_ui.print_status()
            while True:
                # Check if termination is requested
                if state.terminate:
                    print("Terminating Texter...")
                    break  # Exit the loop to stop the thread

                text = recognize_speech(recognizer, source)
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

                    if text.startswith("type"):
                        if state.typing_active:
                            gui.typewrite(text[5:])
                    else:
                        if text == "terminate texter":
                            break
                        if not state.handle_command(text, keyboard_commands, info_commands, selection_commands):
                            if state.typing_active:
                                gui.typewrite(text)


def print_all_commands(): # TODO: CRETE VOICE COMMAND TO PRINT SPECIFIC COMMANDS
    with open('config.json', 'r') as f:
        config = json.load(f)

    for command_type in config:
        if command_type not in ["key_mappings", "programming_language",
                                "speech_engine", "sensitivity", "typing_delay"]:
            print("┌────────────────────────────┐")
            print(f"│ {command_type}:")
            print("├────────────────────────────┤")
            for command in config[command_type]:
                for key, val in command.items():
                    if key == "name": # "command_type":
                        print(f"│ {val}", end=" ")
                print()
            print("└────────────────────────────┘\n")
