"""
This module defines functions to retrieve and manage browser commands from JSON files and to handle browser interactions.

Functions:
- `get_commands(directory: str) -> dict`:
  Retrieves and combines commands from all JSON files in the specified directory.

  Parameters:
  - `directory` (str): Path to the directory containing the JSON files.

  Returns:
  - `dict`: A dictionary containing the combined commands from all found JSON files.

  Error Handling:
  - Returns an empty dictionary if the directory is invalid.
  - Prints an error message for missing or invalid JSON files but continues processing other files.

  Example Usage:
  ```python
  commands = get_commands("/path/to/commands/directory")
  ```

- `focus_browser_window(browser: str = "Chrome") -> None`:
  Attempts to focus an existing browser window based on the provided name.

  Parameters:
  - `browser` (str, optional): The name of the browser window to focus. Defaults to "Chrome".

  Error Handling:
  - Uses `text_to_speech` to notify the user if no matching window is found.
  - Calls `start_browser` to open the browser if it is not found.

- `start_browser(browser: str = "chrome", url: str = None) -> None`:
  Starts Chrome or Firefox browser and optionally opens a specific URL.

  Parameters:
  - `browser` (str): The browser to start ("chrome" or "firefox").
  - `url` (str, optional): The URL to open in the browser.

  Error Handling:
  - Prints an error if the browser is not supported or not installed.
  - Handles unexpected exceptions gracefully.
"""

import glob
import json
import os
import subprocess
from src.utils.text_to_speech import text_to_speech
import logging
from logging_config import setup_logging
setup_logging()
warning_logger = logging.getLogger('warning_logger')
error_logger = logging.getLogger('error_logger')


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
        error_logger.error(f"{directory} does not exist or is not a valid directory")
        return {}

    commands = {}
    # Find all JSON files ending with commands in the specified directory
    json_files = glob.glob(os.path.join(directory, "**", "*commands.json"), recursive=True)

    for file in json_files:
        try:
            with open(file, "r") as f:
                file_commands = json.load(f)
                # Merge commands from each file
                commands.update(file_commands)
        except FileNotFoundError:
            warning_logger.warning(f"Commands file {file} not found.")
        except json.JSONDecodeError:
            error_logger.error(f"Invalid JSON format in commands file {file}.")

    return commands

def focus_browser_window(browser="Chrome") -> None:
    """
    Attempts to focus an existing browser window based on the provided name.

    Args:
        browser (str, optional): The name of the browser window to focus. Defaults to "Chrome".
    """
    try:
        # Search for the browser window
        result = subprocess.run(
            ["xdotool", "search", "--name", browser],
            capture_output=True,
            text=True
        )
        window_id = result.stdout.splitlines()[0]  # Get the first matching window ID

        # Focus the window
        subprocess.run(["xdotool", "windowactivate", window_id])
    except IndexError:
        text_to_speech(f"No open {browser} window found. starting {browser}")
        start_browser(browser)
    except Exception as e:
        error_logger.error(f"Error: {e}")

def start_browser(browser="chrome", url=None) -> None:
    """
    Starts Chrome or Firefox browser. Optionally opens a specific URL.

    Args:
        browser (str): Either "chrome" or "firefox".
        url (str): Optional URL to open in the browser.
    """
    try:
        if browser.lower() == "chrome":
            command = ["google-chrome"]
        elif browser.lower() == "firefox":
            command = ["firefox"]
        else:
            print("Unsupported browser. Use 'chrome' or 'firefox'.")
            return

        # Add URL to command if provided
        if url:
            command.append(url)

        # Run the command
        subprocess.Popen(command)
        print(f"Started {browser} successfully.")
    except FileNotFoundError:
        error_logger.error(f"Error: {browser.capitalize()} is not installed or not in PATH.")
    except Exception as e:
        error_logger.error(f"An error occurred: {e}")