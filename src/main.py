# Standard library imports
import threading

# Local application imports
from AppState import AppState
from TexterUI import TexterUI
from SpeechRecognitionUtils import *


# Serpent
def run_live_speech_interpreter(state, app_ui, keyboard_commands, info_commands, selection_commands, recognizer):
    """
    This function runs the live speech interpreter in a separate thread.
    """
    while not state.terminate:
        live_speech_interpreter(state, app_ui, keyboard_commands, info_commands, selection_commands, recognizer)

def main():
    """
    Initializes the application state and starts the live speech interpreter.

    This function sets up the application by creating an instance of `AppState`, loading
    the necessary command configurations, and initializing the speech recognizer. It then
    begins the live speech interpretation process, which listens for and handles voice commands.
    """
    app = TexterUI()
    state = AppState(app)

    with open("config.json", 'r') as f:
        config = json.load(f)

    keyboard_commands, info_commands, selection_commands = state.load_commands(config)
    recognizer = sr.Recognizer()

    # Create a thread for the live speech interpreter
    speech_thread = threading.Thread(target=run_live_speech_interpreter,
                                     args=(state, app, keyboard_commands, info_commands, selection_commands,
                                           recognizer))
    app.speech_thread = speech_thread
    speech_thread.start()

    # Initialize TexterUI with the state object
    app.init_ui(state, config)



if __name__ == "__main__":
    main()
