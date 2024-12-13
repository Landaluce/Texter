import datetime
import glob
import json
import os
import subprocess

from gtts import gTTS
from word2number import w2n


def get_commands(directory: str):
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


def numeric_str_to_int(numeric_str):
    """
    Converts a numeric string to an integer.

    Parameters:
    - numeric_str (str): The numeric string (e.g., "three") to convert.

    Returns:
    - int: The corresponding integer value.
    """
    numeric_str = numeric_str.split(" ")
    nums = [str(w2n.word_to_num(w)) for w in numeric_str]
    return int("".join(nums))


def convert_to_spelling(text: str, spelling_commands: list) -> str:
    """
    Convert spoken words to corresponding spelling characters.

    Parameters:
        text (str): The command text to process.
        spelling_commands (dict): spelling commands
    Returns:
        eg:
            input text: alpha beta
            output: ab
    """
    words = text.split()
    output = []
    for word in words:
        for command in spelling_commands:
            if command.name == word:
                output.append(command.key)
                break
    return "".join(output)


def string_to_camel_case(input_str: str, lower: bool = False) -> str:
    """Capitalizes the first letter of each word in a string.

    Parameters:
      input_str: The input string.
      lower (bool): indicates if the first word should be capitalized
    Returns:
      The string with the first letter of each word capitalized.
    """
    words = input_str.split()
    capitalized_words = [word.capitalize() for word in words]
    if lower:
        capitalized_words[0] = capitalized_words[0].lower()
    result = "".join(capitalized_words)

    return result


def string_to_snake_case(input_str):
    """
    Convert a given string to snake_case format.

    Parameters:
    - input_str (str): The input string to be converted, where words are typically separated by spaces.

    Returns:
    - str: The converted string in snake_case format, where spaces are replaced by underscores.
    """
    return input_str.replace(" ", "_")

def text_to_speech(text="testing"):
    tts = gTTS(text, lang='en')
    tts.save("output.mp3")
    # os.system("mpg321 -q output.mp3")
    with open("log.txt", "w") as log:
        subprocess.run(["mpg321", "output.mp3"], stdout=log, stderr=log)

def get_current_time() -> str:
    now = datetime.datetime.now()
    return now.strftime("%H:%M")

def get_current_date() -> str:
    now = datetime.datetime.now()
    return now.strftime("%m-%d")


def month_number_to_name(month_number):
    # List of month names, indexed from 0 (January)
    months = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]

    # Check if the month_number is valid (between 1 and 12)
    if 1 <= month_number <= 12:
        return months[month_number - 1]
    else:
        return "Invalid month number"

def day_number_to_name(day_number):
    # Determine the suffix for the day number
    if 10 <= day_number % 100 <= 20:
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(day_number % 10, "th")

    # Return the day number with its ordinal suffix
    return f"{day_number}{suffix}"
