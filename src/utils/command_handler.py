"""
This module contains functions for handling user commands based on the application's mode.

It includes functions to process text in spelling mode and dictation mode,
interpreting commands and writing output as needed.
"""
from __future__ import annotations

from src.commands.text_processor import TextProcessor
from src.utils.gui_utils import write
from src.utils.string_utils import convert_to_spelling, string_to_camel_case, string_to_snake_case


def handle_spelling_mode(app_state, text: str) -> None:
    """
    processes text in spelling mode by converting it to its spelled-out equivalent
    and applying the necessary replacements.

    Args:
        app_state: The application's state, containing spelling-related configurations.
        text (str): The input text to be processed.
    """
    spelling_output = convert_to_spelling(text, app_state.spelling_commands)
    if spelling_output:
        write(spelling_output)


def handle_dictation_mode(app_state, texter_ui, text: str) -> None:
    """Processes text in dictation mode."""
    if text.startswith("camel case") or text.startswith("camelcase"):
        write(string_to_camel_case(text[len("camel case") + 1:]))
    elif text.startswith("small camel case"):
        write(string_to_camel_case(text[len("small camel case") + 1:], True))
    elif text.startswith("snake case"):
        write(string_to_snake_case(text[len("snake case") + 1:].strip()))
    elif text == "terminate texter":
        print("Terminating Texter...")
        app_state.terminate = True
        texter_ui.terminate_all_threads()
    elif not app_state.handle_command(text):
        if app_state.typing_active:
            if app_state.punctuation:
                text_processor = TextProcessor()
                text = text_processor.restore_punctuation(text)
                if app_state.capitalize:
                    text = text_processor.capitalize_sentences(text)
            write(text)
