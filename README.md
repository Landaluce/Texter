# Texter Application

Texter is a voice-controlled application that allows users to perform various actions through speech commands. The app integrates with speech recognition to simulate keyboard and programming operations, making it easy for users to type, select, and execute commands without using a physical keyboard.

## Current Features

- **Voice-Controlled Commands**: Control the app with your voice for typing, programming, and terminal operations.
- **Programming Mode**: Supports Python and Java with pre-configured commands to create classes, functions, and more.
- **Terminal Mode**: Interact with terminal commands (Linux/Windows) via voice input.
- **UI-Based**: Uses Tkinter for an intuitive user interface with status updates.
- **Customizable**: Configure your own commands in the `commands.json` file.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Landaluce/Texter/
   cd Texter
2. Create virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   pip install .

## Usage

1. **Start Texter:** python main.py
2. **Use voice commands like:**  
   - **Wake Up / Go to Sleep**: Activate or deactivate typing and command execution by using the voice commands "Wake Up" and "Go to Sleep".
   - **Programming Mode**: Use "Switch to Python" or "Switch to Java" to change the programming language, and voice commands like "Create class" or "Print statement" for code generation.
   - **Terminal Mode**: Use "Switch to Linux" or "Switch to Windows" to interact with your operating system's terminal commands.
3. **Command Extensions**: To add new custom commands check [this guide](docs/EXTENDING_COMMANDS.md)

## How To Contribute
check [this guide](docs/CONTRIBUTING.md)