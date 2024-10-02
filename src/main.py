# Local application imports
from SpeechRecognitionUtils import *


def run_live_speech_interpreter(app_state, app_ui, recognizer) -> None:
    """
    This function runs the live speech interpreter in a separate thread.
    """
    while not app_state.terminate:
        live_speech_interpreter(app_state, app_ui, recognizer)

def get_commands(file):
    try:
        with open(file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Configuration file not found.")
        return None
    except json.JSONDecodeError:
        print("Invalid JSON format in configuration file.")
        return None

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

    # get commands from json
    config = get_commands(config_file_path)

    app_state.load_commands(config)
    recognizer = sr.Recognizer()

    # Create a thread for the live speech interpreter
    speech_thread = threading.Thread(target=run_live_speech_interpreter,
                                     args=(app_state, app, recognizer))
    # Initialize live speech interpreter thread
    app.speech_thread = speech_thread
    speech_thread.start()

    # Initialize TexterUI with the app_state object
    app.init_ui(app_state, config)



if __name__ == "__main__":
    main()
