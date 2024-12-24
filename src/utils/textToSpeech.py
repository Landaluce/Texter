import os
import subprocess
from gtts import gTTS


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

