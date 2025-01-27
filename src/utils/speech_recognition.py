from __future__ import annotations

from typing import Optional

import speech_recognition as sr
import threading  # noqa: F401
import logging
from logging_config import setup_logging
setup_logging()


def recognize_speech(recognizer: sr.Recognizer, timeout: int = 2) -> Optional[str]:
    """
    Recognizes and returns the speech from the given audio source using the specified recognizer.

    Parameters:
        recognizer (sr.Recognizer): The speech recognition object used to process the audio.
        timeout (int): Maximum number of seconds to wait for speech input before giving up.
                       If no speech is detected within this period, a WaitTimeoutError is raised.

    Returns:
        str: The recognized text, or None if recognition fails.
    """
    with sr.Microphone() as source:
        try:
            audio = recognizer.listen(source, timeout=timeout)
            text = recognizer.recognize_google(audio).lower()
            logging.info(f"voice input: {text}")
            return text

        except sr.UnknownValueError:
            logging.warning("Could not understand audio (sr.UnknownValueError)")
            pass
        except sr.RequestError as e:
            logging.error(f"Error from Speech Recognition service: {e}")
            return None
        except sr.WaitTimeoutError:
            logging.error("waiting time error")
            return None
        except Exception as e:
            logging.error(f"unexpected error: {e}")
            return None
    return None
