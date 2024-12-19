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


def numeric_str_to_int(numeric_str:str) -> int:
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


def string_to_snake_case(input_str:str) -> str:
    """
    Convert a given string to snake_case format.

    Parameters:
    - input_str (str): The input string to be converted, where words are typically separated by spaces.

    Returns:
    - str: The converted string in snake_case format, where spaces are replaced by underscores.
    """
    return input_str.replace(" ", "_")

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

def get_current_time() -> str:
    """
    Retrieves the current time in 24-hour format.

    Returns:
        str: The current time as a string in the format "HH:MM" (e.g., "14:30").
    """
    now = datetime.now()
    return now.strftime("%H:%M")

def get_day_of_week(date_str: str, date_format:str="%Y-%m-%d") -> str:
    """
    Get the day of the week for a given date.

    Args:
        date_str (str): The date as a string (e.g., '2024-12-16').
        date_format (str): The format of the input date string.

    Returns:
        str: The day of the week (e.g., 'Monday').
    """
    date_obj = datetime.strptime(date_str, date_format)  # Convert string to datetime object
    return date_obj.strftime("%A")

def get_current_date() -> datetime:
    """
     Retrieves the current date and time as a `datetime` object.

    Returns:
        datetime: The current date and time.
    """
    return datetime.now()


def month_number_to_name(month_number:int) -> str:
    """
     Converts a numeric month (1-12) to its corresponding month name.

    Args:
        month_number (int): The numeric representation of a month (1 for January, 2 for February, etc.).

    Returns:
        str: The name of the month if the input is valid, or "Invalid month number" if the input is out of range.

    """
    months = [
        "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November",
        "December"
    ]
    if 1 <= month_number <= 12:
        return months[month_number - 1]
    else:
        return "Invalid month number"

def day_number_to_name(day_number:int) -> str:
    """
        Converts a day number (e.g., 1, 2, 3) into its ordinal representation (e.g., 1st, 2nd, 3rd).

        Args:
            day_number (int): The day number to be converted.

        Returns:
            str: The day number with its ordinal suffix.
    """
    if 10 <= day_number % 100 <= 20:
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(day_number % 10, "th")

    return f"{day_number}{suffix}"
