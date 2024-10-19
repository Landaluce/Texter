from word2number import w2n


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
    return int(''.join(nums))


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
    return ''.join(output)


def string_to_camel_case(input_str: str, lower: bool=False) -> str:
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
    return input_str.replace(" ", "_")[1:]
