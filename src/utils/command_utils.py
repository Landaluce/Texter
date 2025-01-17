"""
This module defines the `get_commands` function, which retrieves and combines commands from all JSON files in a specified directory.

The function searches for all JSON files in the given directory whose filenames end with 'commands.json' and loads the
commands from each of these files. The loaded commands are merged into a single dictionary, which is then returned.

Methods:
- `get_commands(directory: str) -> dict`:
    Retrieves commands from all JSON files in the specified directory.

    Parameters:
    - `directory` (str): The path to the directory containing the command JSON files.

    Returns:
    - `dict`: A dictionary containing the combined commands from all found JSON files.

    Error Handling:
    - If the directory does not exist or is invalid, the function returns an empty dictionary.
    - If a file is not found or cannot be parsed as JSON, the function prints an error message and continues processing other files.

Example Usage:
    commands = get_commands("/path/to/commands/directory")
"""

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