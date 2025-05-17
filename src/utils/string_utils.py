"""
This module provides various utility functions for string manipulations, number extractions, and text conversions.

Functions:
- `numeric_str_to_int`: Converts a numeric string (e.g., "three") to its corresponding integer value.
    - Args:
        - `numeric_str` (str): The numeric string (e.g., "three") to convert.
    - Returns:
        - `int`: The corresponding integer value.

- `convert_to_spelling`: Converts spoken words (e.g., "alpha", "beta") to corresponding spelling characters.
    - Args:
        - `text` (str): The input text (e.g., "alpha beta") to process.
        - `spelling_commands` (list): A list of spelling commands mapping words to their corresponding letters.
    - Returns:
        - `str`: A string containing the converted spelling characters (e.g., "ab").

- `string_to_camel_case`: Converts a string to camelCase, with an option to lowercase the first word.
    - Args:
        - `input_str` (str): The input string to convert.
        - `lower` (bool): If True, the first word will be lowercase. Defaults to False.
    - Returns:
        - `str`: The input string in camelCase format.

- `string_to_snake_case`: Converts a given string to snake_case format.
    - Args:
        - `input_str` (str): The input string to be converted.
    - Returns:
        - `str`: The string in snake_case format, where spaces are replaced with underscores.

- `extract_number_from_string`: Extracts and returns a numeric value from the input text.
    - Args:
        - `text` (str): The command text from which to extract the number.
    - Returns:
        - `int`: The extracted numeric value, or 1 if extraction fails.
"""
from word2number import w2n
import speech_recognition as sr

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
    word_to_key = {command.name: command.action for command in spelling_commands}
    return "".join(word_to_key.get(word, "") for word in text.split())

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

def extract_number_from_string(text: str) -> int:
    """
    Extracts and returns a numeric value from the command text.

    Parameters:
    - text (str): The command text from which to extract the number.

    Returns:
    - int: The extracted numeric value, or 1 if extraction fails due to parsing errors.
    """
    try:
        if ":" in text:
            return int(text.split(":")[0])
        elif text.isdigit():
            return int(text)
        else:
            return numeric_str_to_int(text)
    except (ValueError, sr.UnknownValueError):
        return 1