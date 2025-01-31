"""
This module provides utilities for simulating keyboard interactions using the `pyautogui` library.

Functions:
- `press(keyboard_key: str) -> None`:
  Simulates pressing a single keyboard key.

  Parameters:
  - `keyboard_key` (str): The key to press.

  Example Usage:
  ```python
  press("enter")
  ```

- `write(text: str) -> None`:
  Simulates typing a string of text.

  Parameters:
  - `text` (str): The text to type.

  Example Usage:
  ```python
  write("Hello, world!")
  ```
"""
import pyautogui as gui

def press(keyboard_key: str, count: int=1) -> None:
    """
    Simulates pressing a single keyboard key.

    Parameters:
    - keyboard_key (str): The key to press.
    """
    for _ in range(0, count):
        gui.hotkey(keyboard_key)

def write(text: str) -> None:
    """
    Simulates typing a string of text.

    Parameters:
    - text (str): The text to type.
    """
    gui.write(text)

def scroll(pixels: int) -> None:
    """
    Simulates scrolling by a specified number of pixels.

    Parameters:
    - pixels (int): The number of pixels to scroll. Positive values scroll up, and negative values scroll down.
    """
    gui.scroll(pixels)
