# Local application imports
from helperFunctions import get_commands
from SpeechRecognitionUtils import *


def main():
    """
    Initializes the application app_state and starts the live speech interpreter.

    This function sets up the application by creating an instance of `AppState`, loading
    the necessary commands, and initializing the speech recognizer. It then
    begins the live speech interpretation process, which listens for and handles voice commands.
    """
    app = TexterUI()
    app_state = AppState(app)

    command_files_directory = "speech_commands"

    # Get commands from all relevant JSON files in the directory
    commands = get_commands(command_files_directory)

    app_state.load_commands(commands)
    recognizer = sr.Recognizer()

    # Create a thread for the live speech interpreter
    speech_thread = threading.Thread(target=run_live_speech_interpreter,
                                     args=(app_state, app, recognizer))
    # Initialize live speech interpreter thread
    app.speech_thread = speech_thread
    speech_thread.start()

    # Initialize TexterUI
    app.init_ui(app_state, commands)


if __name__ == "__main__":
    main()
