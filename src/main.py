"""
Main function that initializes the application state and starts the live speech interpreter.

This function sets up the application by performing the following tasks:
- Creates an instance of `AppState` and initializes the UI.
- Loads the necessary commands using the `get_commands` function.
- Sets up the speech recognizer using the `speech_recognition` library.
- Starts the live speech interpretation process in a separate thread to handle speech commands in real-time.

Example Usage:
    Run the script to initialize the application, load commands, and start live speech recognition.

Raises:
    RuntimeError: If the commands cannot be loaded or if the speech interpreter thread fails to start.
"""
from utils.command_utils import get_commands
from src.utils.speech_recognition_utils import *


def main():
    """
    Initializes the application app_state and starts the live speech interpreter.
    This function sets up the application by:
    - Creating an instance of `AppState`
    - Loading the necessary commands.
    - Initializing the speech recognizer.
    - Starting the live speech interpretation process in a separate thread.

    Example Usage:
        Run the script to start the application and speech recognition.

    Raises:
        RuntimeError: If commands cannot be loaded or threads fail to start.
    """
    command_files_directory = "speech_commands"

    try:
        app = TexterUI(command_files_directory)
        recognizer = sr.Recognizer()
        app_state = AppState(app)

        # Load commands
        commands = get_commands(command_files_directory)
        app_state.load_commands(commands)

        # Start live speech interpreter thread
        speech_thread = threading.Thread(
            target=run_live_speech_interpreter, args=(app_state, app, recognizer), daemon=True
        )
        app.speech_thread = speech_thread
        speech_thread.start()

        # Initialize UI
        app.init_ui(app_state, commands)

    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
