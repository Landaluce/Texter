# Local application imports
from src.helperFunctions import get_commands
from src.SpeechRecognitionUtils import *


def main():
    """
        Initializes the application app_state and starts the live speech interpreter.
    __init__
        This function sets up the application by creating an instance of `AppState`, loading
        the necessary commands, and initializing the speech recognizer. It then
        begins the live speech interpretation process, which listens for and handles voice commands.
    """
    command_files_directory = "speech_commands"

    app = TexterUI(command_files_directory)
    recognizer = sr.Recognizer()
    app_state = AppState(app)
    commands = get_commands(command_files_directory)
    app_state.load_commands(commands)

    speech_thread = threading.Thread(
        target=run_live_speech_interpreter, args=(app_state, app, recognizer)
    )
    app.speech_thread = speech_thread
    speech_thread.start()

    app.init_ui(app_state, commands)


if __name__ == "__main__":
    main()
