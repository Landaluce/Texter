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

        This method creates the main window and initializes elements such as buttons, labels, and text boxes.
        It sets default attributes like `state`, `commands_label`, `input_text_box`, `status_label`, and more.
        """
        self.command_files_directory = command_files_directory
        self.root = tk.Tk()
        self.root.title("Texter")

        self.app_state = None
        self.background_color = "black"
        self.font_color = "white"
        self.imgs_path = f"{os.path.abspath('../src/imgs/')}/"

        # initialize window's dimensions
        self.window_width = 300
        self.window_height = 600
        self.window_position_x = 100
        self.window_position_y = 100

        # set label dimensions
        self.label_width = 280
        self.label_height = 15

        # set text_boxs dimensions
        self.input_height = 100
        self.status_height = 100
        self.commands_height = 255

        # set collapse/expand settings
        self.collapsed_geometry = f"300x330"
        self.expanded_geometry = f"300x605"
        self.collapsed_commands_height = 0


        # initialize ui element
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
        Initializes the Texter user interface with input elements, buttons, and labels based on the provided state and
        commands.

        Parameters:
            app_state (AppState): The current state of the user interface.
            commands (dict): dictionary with commands
        """
        self.app_state = app_state
        self.commands = commands

        # Override the close window button
        self.root.protocol("WM_DELETE_WINDOW", self.on_terminate_button_click)

        # Make the window always on top
        self.root.attributes("-topmost", True)

        self.configure_window()
        self.configure_input_section()
        self.configure_action_buttons()
        self.configure_status_section()
        self.configure_commands_section()

        # Create the main window
        self.root.mainloop()

    def configure_window(self):
        """Set the dimensions, position, and appearance of the main window."""
        self.root.geometry(
            f"{self.window_width}x{self.window_height}+{self.window_position_x}+{self.window_position_y}")
        self.root.resizable(False, False)
        self.root.pack_propagate(False)
        self.root.configure(bg=self.background_color)

    def configure_input_section(self):
        """Create the input section of the UI."""
        # Create Input label
        self.commands_label = tk.Label(self.root, text="Input", fg=self.font_color)
        self.commands_label.configure(bg=self.background_color)
        self.commands_label.place(x=10, y=5, width=self.label_width, height=self.label_height)

        self.input_text_box = tk.Text(self.root, wrap=tk.WORD, padx=0, fg=self.font_color, bg=self.background_color)
        self.input_text_box.place(x=0, y=25, width=self.window_width, height=self.input_height)
        self.input_text_box.config(state=tk.DISABLED)  # Make the text box non-editable

    def configure_action_buttons(self):
        """Create action buttons (Wake Up, Go to Sleep, Quit)."""
        self.wake_up_button = tk.Button(self.root, text="▶", command=self.on_wake_up_button_click, fg=self.font_color,
                                        bg=self.background_color)
        self.wake_up_button.place(x=10, y=130)#, width=25, height=25)

        self.go_to_sleep_button = tk.Button(self.root, text="||", fg=self.font_color, bg=self.background_color,
                                            command=self.on_go_to_sleep_button_click,)
        self.go_to_sleep_button.place(x=50, y=130)

        self.terminate_button = tk.Button(self.root, text="◼", fg=self.font_color, bg=self.background_color,
                                          command=self.on_terminate_button_click,)
        self.terminate_button.place(x=90, y=130)

    def configure_status_section(self):
        """Create the status section of the UI."""
        self.status_label = tk.Label(
            self.root,
            borderwidth=5,
            fg=self.font_color,
            text="Status" if self.app_state.typing_active else "Typing: Stopped",
        )
        self.status_label.configure(bg=self.background_color)
        self.status_label.place(x=10, y=165, width=self.label_width, height=self.label_height)

        self.status_text_box = tk.Text(self.root, fg=self.font_color, bg=self.background_color)
        self.print_status()
        self.status_text_box.config(state=tk.DISABLED)
        self.status_text_box.place(x=0, y=185, width=self.window_width, height=self.status_height)

    def configure_commands_section(self):
        """Create the commands section of the UI."""
        # Create Commands label
        self.commands_label = tk.Label(self.root, text="Commands", fg=self.font_color)
        self.commands_label.configure(bg=self.background_color)
        self.commands_label.place(x=0, y=300, width=self.label_width, height=self.label_height)

        # Create expand/collapse button
        self.toggle_commands_button = tk.Button(self.root, text="▲", command=self.toggle_status_textbox,
                                                bg=self.background_color, fg=self.font_color,)
        self.toggle_commands_button.place(x=10, y=295)#, width=25, height=25)

        # Create a non-editable text box: commands
        self.commands_text_box = tk.Text(self.root,fg=self. font_color, bg=self.background_color)
        self.print_all_commands()
        self.commands_text_box.config(state=tk.DISABLED)
        self.commands_text_box.place(x=0, y=330, width=self.window_width, height=self.commands_height)

    def reload_commands(self):  # TODO: remove/add reload commands
        """Reload the commands from the updated commands file and display them in the UI."""
        # Clear the commands text box
        self.commands_text_box.commands(state=tk.NORMAL)
        self.commands_text_box.delete(1.0, tk.END)

        # commands = get_commands(self.command_files_directory)

        # Re-display the commands
        self.print_all_commands()
        self.commands_text_box.commands(state=tk.DISABLED)

    def toggle_status_textbox(self):
        """Toggle between expanding and collapsing the Text widget."""
        if self.commands_text_box.winfo_height() == self.commands_height:
            self.commands_text_box.place(width=self.window_width, height=self.collapsed_commands_height)
            self.toggle_commands_button.config(text="▼")
            self.root.geometry(self.collapsed_geometry)  # Collapse window
        else:
            self.commands_text_box.place(width=self.window_width, height=self.commands_height)
            self.toggle_commands_button.config(text="▲",)
            self.root.geometry(self.expanded_geometry)  # Expand window

    def on_terminate_button_click(self) -> None:
        """
        Set the termination flag to True, and destroy the main window.
        """
        self.app_state.terminate = True  # Signal all threads to terminate
        if hasattr(self, "speech_thread") and self.speech_thread.is_alive():
            self.speech_thread.join()  # Wait for the thread to finish
        self.root.destroy()  # Close the UI

    def terminate_all_threads(self):
        """
        Safely terminates the speech thread and exits the main thread.
        """
        try:
            # Set the termination flag to stop the live interpreter
            self.app_state.terminate = True
            # Ensure the speech thread is joined (wait for it to finish)
            if hasattr(self, "speech_thread") and self.speech_thread.is_alive():
                self.speech_thread.join()
            sys.exit(0)  # Terminate the main thread and exit the program
        except AttributeError as e:
            # Handle the case where the speech_thread attribute is missing
            error_logger.error(f"Error: {e}")
        except Exception as e:
            # Catch any other unexpected exceptions
            error_logger.error(f"Unexpected error: {e}")

    def on_wake_up_button_click(self) -> None:
        """
        Activates the typing mode by setting 'typing_active' to True in the current state and updates the UI status.
        """
        self.app_state.typing_active = True
        self.app_state.update_status()

    def on_go_to_sleep_button_click(self) -> None:
        """
        Deactivates the typing mode by setting 'typing_active' to False in the current state and updates the UI status.
        """
        self.app_state.typing_active = False
        self.app_state.update_status()

    def get_active_commands(self):
        """Get active commands to display in the UI"""
        active_commands = {}

        def process_commands(commands, type_name):
            """Creates a list of commands"""
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
        """Format commands as a string block for display."""
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
        """
        Display the active commands in the user interface based on the provided commands.

        Returns:
            None
        """
        commands = self.get_active_commands()
        for command_type, command_list in commands.items():
            self.commands_text_box.insert(tk.END, self.format_command_block(command_type, command_list))

    def print_status(self) -> None:
        """
        Updates the UI to reflect the current status.
        """
        self.app_state.update_status()

    def append_text(self, text: str) -> None:
        """
        Appends text to the input text box.

        Parameters:
        - text (str): The string to be appended to the text box.

        This method enables the text box temporarily for editing, adds the text,
        scrolls to the end, and then disables the text box to make it non-editable again.
        """
        self.input_text_box.config(state=tk.NORMAL)  # Enable editing to insert text
        self.input_text_box.insert(tk.END, text + "\n")  # Append the message
        self.input_text_box.see(tk.END)  # Scroll to the end
        self.input_text_box.config(state=tk.DISABLED)  # Disable editing again

    def update_status(self, status_message: str) -> None:
        """
        Thread-safe update to the status_text_box.
        """
        self.root.after(0, self._update_status_ui, status_message)

    def _update_status_ui(self, status_message: str) -> None:
        """
        Updates the status_text_box with the latest status message.
        """
        self.status_text_box.config(state=tk.NORMAL)  # Enable editing to insert text
        self.status_text_box.delete(1.0, tk.END)  # Clear the current content
        self.status_text_box.insert(tk.END, status_message)  # Insert new status
        self.status_text_box.config(state=tk.DISABLED)  # Disable editing again

    def update_commands(self) -> None:
        """
        Thread-safe update to the status_text_box.
        """
        # noinspection PyTypeChecker
        self.root.after(0, self._update_commands_ui)

    def _update_commands_ui(self) -> None:
        """
        Updates the status_text_box with the latest status message.
        """
        self.commands_text_box.config(state=tk.NORMAL)  # Enable editing to insert text
        self.commands_text_box.delete(1.0, tk.END)  # Clear the current content
        self.print_all_commands()
        self.commands_text_box.config(state=tk.DISABLED)  # Disable editing again
