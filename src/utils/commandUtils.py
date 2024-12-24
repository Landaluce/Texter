import glob
import json
import os


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