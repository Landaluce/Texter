from setuptools import setup, find_packages

setup(
    name='your_project_name',  # Replace with your project name
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'PyAutoGUI',
        'SpeechRecognition',
        'word2number'
    ],
)