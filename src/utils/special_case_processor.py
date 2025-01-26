from __future__ import annotations

from src.constants.speech_recognition_constants import replacements


def process_special_cases(text: str) -> str:
    """
    Handles special case replacements in recognized text.

    Args:
        text (str): The input text to process.

    Returns:
        str: The processed text with replacements applied.

    Raises:
        ValueError: If the input is not a string.
    """
    if not isinstance(text, str):
        raise ValueError(f"Expected 'txt' to be a string, but got {type(text)}")

    for target, replacement in replacements.items():
        text = text.replace(target, replacement)
    return text
