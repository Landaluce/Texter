# Local application imports
import glob
import os

from SpeechRecognitionUtils import *


def run_live_speech_interpreter(app_state: AppState, app_ui: TexterUI, recognizer) -> None:
    """
    This function runs the live speech interpreter in a separate thread.
    """
    while not app_state.terminate:
        live_speech_interpreter(app_state, app_ui, recognizer)


def get_commands(directory: str):
    """
    Retrieves commands from all JSON files in the given directory with filenames ending in 'commands'.
    """
    commands = {}
    # Find all JSON files ending with commands in the specified directory
    json_files = glob.glob(os.path.join(directory, '*commands.json'))

    for file in json_files:
        try:
            with open(file, 'r') as f:
                file_commands = json.load(f)
                # Merge commands from each file
                commands.update(file_commands)
        except FileNotFoundError:
            print(f"Commands file {file} not found.")
        except json.JSONDecodeError:
            print(f"Invalid JSON format in commands file {file}.")

    return commands


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
