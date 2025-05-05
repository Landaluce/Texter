"""

This module defines the `TexterUI` class, which provides a graphical user interface (GUI) for the Texter application.

The GUI allows users to interact with the app by entering text commands, controlling typing modes, and displaying status and active commands.

The interface is built using the `tkinter` library and includes various buttons, labels, and text boxes for interaction.



Key Features:

1. **Interactive Commands**: Users can view, add, or interact with various command types (e.g., info, selection, programming).

2. **Status Display**: A section of the interface shows the current status of the app, including typing mode and other relevant information.

3. **Window Control**: Includes buttons to manage the app's state (e.g., wake up, go to sleep, terminate).

4. **Text Input**: A non-editable text box displays input, while allowing users to append text programmatically.



Methods:

- `__init__(self, command_files_directory)`:

Initializes the `TexterUI` instance, setting up attributes and initializing the window.



- `load_image(filename)`:

Loads and resizes an image for use in buttons (e.g., wake up, terminate).



- `init_ui(self, app_state, commands)`:

Initializes the user interface, setting up input elements, buttons, labels, and status sections based on the app's state and commands.



- `configure_window(self)`:

Configures the main window's dimensions, position, and appearance.



- `create_input_section(self)`:

Creates the section of the UI where input is displayed.



- `create_action_buttons(self)`:

Creates buttons for various actions (e.g., wake up, go to sleep, terminate).



- `create_status_section(self)`:

Creates the status section, displaying information about the app's current state.



- `create_commands_section(self)`:

Creates a section for displaying commands and controlling the display of active commands.



- `reload_commands(self)`:

Reloads commands from an updated file and refreshes the command display.



- `toggle_status_textbox(self)`:

Toggles the visibility of the commands section, expanding or collapsing it.



- `on_terminate_button_click(self)`:

Terminates the application and closes the main window.



- `terminate_all_threads(self)`:

Safely terminates all threads and exits the application.



- `on_wake_up_button_click(self)`:

Activates the typing mode and updates the UI status.



- `on_go_to_sleep_button_click(self)`:

Deactivates the typing mode and updates the UI status.



- `get_active_commands(self)`:

Retrieves all active commands grouped by type (e.g., info commands, git commands).



- `format_command_block(command_type, commands)`:

Formats commands into a string block for display.



- `print_all_commands(self)`:

Displays all active commands in the UI.



- `print_status(self)`:

Updates the UI to reflect the current status of the app.



- `append_text(self, text)`:

Appends text to the input text box and scrolls to the end.



- `update_status(self, status_message)`:

Updates the status text box in a thread-safe manner.



- `update_commands(self)`:

Updates the commands display in a thread-safe manner.



- `_update_status_ui(self, status_message)`:

Updates the status text box with the latest status message.



- `_update_commands_ui(self)`:

Updates the commands text box with the latest list of commands.



Dependencies:

- `tkinter`: The standard Python library for creating GUIs.

- `json`: Used for processing commands as JSON objects.

- `os`, `sys`: Libraries for working with file paths and system functionalities.



Usage Example:

texter_ui = TexterUI(command_files_directory="/path/to/commands")

texter_ui.init_ui(app_state, commands_dict)

"""
import json
import os
import sys
import tkinter as tk
from tkinter import scrolledtext, ttk
import logging

from logging_config import setup_logging

setup_logging()
warning_logger = logging.getLogger('warning_logger')
error_logger = logging.getLogger('error_logger')


class TexterUI:
    """
    A class representing the Texter user interface.
    """

    def __init__(self, command_files_directory):
        """
        Initializes the TexterUI class with attributes for the user interface elements.
        """
        self.command_files_directory = command_files_directory
        self.root = tk.Tk()
        self.root.title("Texter")

        self.app_state = None
        self.background_color = "#282c34"  # Dark background
        self.font_color = "#abb2bf"  # Light font
        self.imgs_path = f"{os.path.abspath('../src/imgs/')}/"

        self.window_width = 400
        self.window_height = 700
        self.window_position_x = 100
        self.window_position_y = 100

        self.label_width = 380
        self.label_height = 25

        self.input_height = 150
        self.status_height = 150
        self.commands_height = 300

        self.collapsed_geometry = f"400x480"  # Adjusted collapsed geometry
        self.expanded_geometry = f"400x705"  # Adjusted expanded geometry
        self.collapsed_commands_height = 0

        self.commands_label = None
        self.input_text_box = None
        self.commands_text_box = None
        self.wake_up_button = None
        self.go_to_sleep_button = None
        self.terminate_button = None
        self.status_label = None
        self.status_text_box = None
        self.toggle_commands_button = None
        self.add_command_button = None
        self.commands = None

    def load_image(self, filename):
        """Load and resize an image."""
        path = os.path.join(self.imgs_path, filename)
        return tk.PhotoImage(file=path)

    def init_ui(self, app_state, commands: dict) -> None:
        """
        Initializes the Texter user interface.
        """
        self.app_state = app_state
        self.commands = commands

        self.root.protocol("WM_DELETE_WINDOW", self.on_terminate_button_click)
        self.root.attributes("-topmost", True)

        self.configure_window()
        self.configure_input_section()
        self.configure_action_buttons()
        self.configure_status_section()
        self.configure_commands_section()

        self.root.mainloop()

    def configure_window(self):
        """Set window dimensions, position, and appearance."""
        self.root.geometry(
            f"{self.window_width}x{self.window_height}+{self.window_position_x}+{self.window_position_y}")
        self.root.resizable(False, False)
        self.root.configure(bg=self.background_color)

    def configure_input_section(self):
        """Create the input section."""
        self.commands_label = tk.Label(self.root, text="Input", fg=self.font_color, bg=self.background_color,
                                       font=("Arial", 12))
        self.commands_label.place(x=10, y=5, width=self.label_width, height=self.label_height)

        self.input_text_box = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, padx=5, pady=5,
                                                               fg=self.font_color, bg="#383e4a",
                                                               insertbackground=self.font_color,
                                                               selectbackground="#515663",
                                                               font=("Consolas", 10))
        self.input_text_box.place(x=0, y=30, width=self.window_width, height=self.input_height)
        self.input_text_box.config(state=tk.DISABLED)

    def configure_action_buttons(self):
        """Create action buttons."""
        style = ttk.Style()
        style.configure("TButton", foreground=self.font_color, background=self.background_color,
                        font=("Arial", 10), padding=5)

        self.wake_up_button = ttk.Button(self.root, text="▶ Wake Up", command=self.on_wake_up_button_click, style="TButton")
        self.wake_up_button.place(x=10, y=190)

        self.go_to_sleep_button = ttk.Button(self.root, text="|| Sleep", command=self.on_go_to_sleep_button_click, style="TButton")
        self.go_to_sleep_button.place(x=120, y=190)

        self.terminate_button = ttk.Button(self.root, text="◼ Terminate", command=self.on_terminate_button_click, style="TButton")
        self.terminate_button.place(x=230, y=190)

    def configure_status_section(self):
        """Create the status section."""
        self.status_label = tk.Label(self.root, text="Status", fg=self.font_color, bg=self.background_color,
                                     font=("Arial", 12))
        self.status_label.place(x=10, y=230, width=self.label_width, height=self.label_height)

        self.status_text_box = scrolledtext.ScrolledText(self.root, fg=self.font_color, bg="#383e4a",
                                                                insertbackground=self.font_color,
                                                                selectbackground="#515663",
                                                                font=("Consolas", 10))
        self.print_status()
        self.status_text_box.config(state=tk.DISABLED)
        self.status_text_box.place(x=0, y=255, width=self.window_width, height=self.status_height)

    def configure_commands_section(self):
        """Create the commands section."""
        self.commands_label = tk.Label(self.root, text="Commands", fg=self.font_color, bg=self.background_color,
                                        font=("Arial", 12))
        self.commands_label.place(x=0, y=410, width=self.label_width, height=self.label_height)

        self.toggle_commands_button = ttk.Button(self.root, text="▲", command=self.toggle_status_textbox)
        self.toggle_commands_button.place(x=10, y=410)

        self.commands_text_box = scrolledtext.ScrolledText(self.root, fg=self.font_color, bg="#383e4a",
                                                                 insertbackground=self.font_color,
                                                                 selectbackground="#515663",
                                                                 font=("Consolas", 10))
        self.print_all_commands()
        self.commands_text_box.config(state=tk.DISABLED)
        self.commands_text_box.place(x=0, y=440, width=self.window_width, height=self.commands_height)

    def reload_commands(self):
        """Reload commands."""
        self.commands_text_box.config(state=tk.NORMAL)
        self.commands_text_box.delete(1.0, tk.END)
        self.print_all_commands()
        self.commands_text_box.config(state=tk.DISABLED)

    def toggle_status_textbox(self):
        """Toggle commands section visibility."""
        if self.commands_text_box.winfo_height() == self.commands_height:
            self.commands_text_box.place(width=self.window_width, height=self.collapsed_commands_height)
            self.toggle_commands_button.config(text="▼")
            self.root.geometry(self.collapsed_geometry)
        else:
            self.commands_text_box.place(width=self.window_width, height=self.commands_height)
            self.toggle_commands_button.config(text="▲")
            self.root.geometry(self.expanded_geometry)

    def on_terminate_button_click(self) -> None:
        """Terminate application."""
        self.app_state.terminate = True
        if hasattr(self, "speech_thread") and self.speech_thread.is_alive():
            self.speech_thread.join()
        self.root.destroy()

    def terminate_all_threads(self):
        """Terminate all threads safely."""
        try:
            self.app_state.terminate = True
            if hasattr(self, "speech_thread") and self.speech_thread.is_alive():
                self.speech_thread.join()
            sys.exit(0)
        except AttributeError as e:
            error_logger.error(f"Error: {e}")
        except Exception as e:
            error_logger.error(f"Unexpected error: {e}")

    def on_wake_up_button_click(self) -> None:
        """Activate typing mode."""
        self.app_state.typing_active = True
        self.app_state.update_status()

    def on_go_to_sleep_button_click(self) -> None:
        """Deactivate typing mode."""
        self.app_state.typing_active = False
        self.app_state.update_status()

    def get_active_commands(self):
        """Get active commands."""
        active_commands = {}

        def process_commands(commands, type_name):
            lst = []
            for command in commands:
                temp_dict = command.commands_to_dict()
                temp_json = json.dumps(temp_dict)
                lst.append(temp_json)
            active_commands[type_name] = lst

        process_commands(self.app_state.info_commands, "info commands")
        process_commands(self.app_state.selection_commands, "selection commands")
        process_commands(self.app_state.git_commands, "git commands")
        process_commands(self.app_state.interactive_commands, "interactive commands")
        process_commands(self.app_state.interactive_commands, "browser commands")

        if self.app_state.programming:
            process_commands(self.app_state.programming_commands, "programming commands")

        if self.app_state.terminal:
            process_commands(self.app_state.terminal_commands, "terminal commands")

        process_commands(self.app_state.spelling_commands, "spelling commands")
        process_commands(self.app_state.keyboard_commands, "keyboard commands")

        return active_commands

    @staticmethod
    def format_command_block(command_type, commands):
        """Format commands for display."""
        block = f"┌{'─' * 34}┐\n"
        block += f"│ {command_type}:\n"
        block += f"├{'─' * 34}┤\n"
        for command in commands:
            for key, val in json.loads(command).items():
                if key == "name":
                    block += f" {val}\n"
        block += f"└{'─' * 34}┘\n"
        return block

    def print_all_commands(self) -> None:
        """Display active commands."""
        commands = self.get_active_commands()
        for command_type, command_list in commands.items():
            self.commands_text_box.insert(tk.END, self.format_command_block(command_type, command_list))

    def print_status(self) -> None:
        """Update UI status."""
        self.app_state.update_status()

    def append_text(self, text: str) -> None:
        """Append text to input box."""
        self.input_text_box.config(state=tk.NORMAL)
        self.input_text_box.insert(tk.END, text + "\n")
        self.input_text_box.see(tk.END)
        self.input_text_box.config(state=tk.DISABLED)

    def update_status(self, status_message: str) -> None:
        """Thread-safe status update."""
        self.root.after(0, self._update_status_ui, status_message)

    def _update_status_ui(self, status_message: str) -> None:
        """Update status text box."""
        self.status_text_box.config(state=tk.NORMAL)
        self.status_text_box.delete(1.0, tk.END)
        self.status_text_box.insert(tk.END, status_message)
        self.status_text_box.config(state=tk.DISABLED)

    def update_commands(self) -> None:
        """Thread-safe commands update."""
        self.root.after(0, self._update_commands_ui)

    def _update_commands_ui(self) -> None:
        """Update commands text box."""
        self.commands_text_box.config(state=tk.NORMAL)
        self.commands_text_box.delete(1.0, tk.END)
        self.print_all_commands()
        self.commands_text_box.config(state=tk.DISABLED)