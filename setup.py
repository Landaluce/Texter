from setuptools import setup, find_packages

setup(
    name="Texter",
    version="0.1",
    packages=find_packages(),
    install_requires=["PyAutoGUI", "SpeechRecognition", "word2number"],
)
