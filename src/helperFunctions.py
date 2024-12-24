from datetime import datetime
import glob
import json
import os
import subprocess

from gtts import gTTS
from word2number import w2n


def get_commands(directory: str) -> dict:
    """
    Retrieves commands from all JSON files in the given directory with filenames ending in 'commands'.

    Parameters:
    - directory (str): The path to the directory containing JSON files with commands.

    Returns:
    - dict: A dictionary of commands combined from all JSON files.
    """
    # Check if directory is valid
    if not os.path.isdir(directory):
        "The specified directory does not exist or is not a valid directory."
        return {}

    commands = {}
    # Find all JSON files ending with commands in the specified directory
    json_files = glob.glob(os.path.join(directory, "*commands.json"))

    for file in json_files:
        try:
            with open(file, "r") as f:
                file_commands = json.load(f)
                # Merge commands from each file
                commands.update(file_commands)
        except FileNotFoundError:
            print(f"Commands file {file} not found.")
        except json.JSONDecodeError:
            print(f"Invalid JSON format in commands file {file}.")

    return commands

def text_to_speech(text:str="testing") -> None:
    """
    Converts a given text string into speech, saves it as an MP3 file,
    and plays it using an external audio player.

    Args:
        text (str): The text to be converted into speech. Defaults to "testing".

    Returns:
        None: This function does not return a value. The output is saved as "output.mp3"
        and played using `mpg321`.
    """
    tts = gTTS(text, lang='en')
    tts.save("output.mp3")
    # os.system("mpg321 -q output.mp3")
    with open("log.txt", "w") as log:
        subprocess.run(["mpg321", "output.mp3"], stdout=log, stderr=log)
    os.remove("log.txt")
    os.remove("output.mp3")

