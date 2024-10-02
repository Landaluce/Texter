# Standard library imports
import threading

# Local application imports
from AppState import AppState
from TexterUI import TexterUI
from SpeechRecognitionUtils import *


# Serpent
def run_live_speech_interpreter(state, app_ui, keyboard_commands, info_commands, selection_commands, recognizer) -> None:
    """
    This function runs the live speech interpreter in a separate thread.
    """
    while not state.terminate:
        live_speech_interpreter(state, app_ui, keyboard_commands, info_commands, selection_commands, recognizer)

def main():
    """
    Initializes the application app_state and starts the live speech interpreter.

    This function sets up the application by creating an instance of `AppState`, loading
    the necessary command configurations, and initializing the speech recognizer. It then
    begins the live speech interpretation process, which listens for and handles voice commands.
    """
    app = TexterUI()
    app_state = AppState(app)
    config_file_path = "config.json"
    # hello

    try:
        with open(config_file_path, 'r') as f:
            config = json.load(f)
    except FileNotFoundError:
        print("Configuration file not found.")
        return None
    except json.JSONDecodeError:
        print("Invalid JSON format in configuration file.")
        return None

    keyboard_commands, info_commands, selection_commands = app_state.load_commands(config)
    recognizer = sr.Recognizer()

    # Create a thread for the live speech interpreter
    speech_thread = threading.Thread(target=run_live_speech_interpreter,
                                     args=(app_state, app, keyboard_commands, info_commands, selection_commands,
                                           recognizer))
    app.speech_thread = speech_thread
    speech_thread.start()

    # Initialize TexterUI with the app_state object
    app.init_ui(app_state, config)



if __name__ == "__main__":
    main()
