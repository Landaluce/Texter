# Standard library imports
import json
import sys
import tkinter as tk

# Local application imports


class TexterUI:
    """
    A class representing the Texter user interface.
    """
    def __init__(self):
        """
        Initializes the TexterUI class with attributes for the user interface elements.

        This method creates the main window and initializes elements such as buttons, labels, and text boxes.
        It sets default attributes like `state`, `commands_label`, `input_text_box`, `status_label`, and more.
        """
        # Create the main window
        self.commands = None
        self.root = tk.Tk()

        self.app_state = None
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

    def init_ui(self, app_state, commands: dict) -> None:
        """
        Initializes the Texter user interface with input elements, buttons, and labels based on the provided state and
        commands.

        Parameters:
            app_state (AppState): The current state of the user interface.
            commands (dict): dictionary with commands
        """
        self.commands = commands
        self.root.protocol("WM_DELETE_WINDOW", self.on_terminate_button_click)  # Override the close window button
        self.root.title("Texter")  # Set the window title

        # Make the window always on top
        self.root.attributes("-topmost", True)

        self.app_state = app_state

        # Set the dimensions and position of the window (width x height + x_offset + y_offset
        self.root.geometry("300x600+100+100")

        # Allow the window to wrap content dynamically
        self.root.pack_propagate(False)

        self.root.configure(bg='darkgray')  # Set background color

        # Create Input label
        self.commands_label = tk.Label(self.root, text="Input")
        self.commands_label.configure(bg='darkgray')
        self.commands_label.place(x=10, y = 5, width=280, height=15)

        # Create a non-editable text box: Input
        self.input_text_box = tk.Text(self.root, wrap=tk.WORD, padx=10, width=280, height=100)
        self.input_text_box.place(x=10, y=25, width=280, height=100)  # Set location and size
        self.input_text_box.config(state=tk.DISABLED)  # Make the text box non-editable

        # Create action buttons: Wake Up, Go to Sleep, Quit
        self.wake_up_button = tk.Button(self.root, text="Wake Up", command=self.on_wake_up_button_click)
        self.wake_up_button.place(x=10, y=130, width=100, height=30)

        self.go_to_sleep_button = tk.Button(self.root, text="Go to Sleep", command=self.on_go_to_sleep_button_click)
        self.go_to_sleep_button.place(x=110, y=130, width=100, height=30)

        self.terminate_button = tk.Button(self.root, text="Quit", command=self.on_terminate_button_click)
        self.terminate_button.place(x=210, y=130, width=80, height=30)

        # Create status label
        self.status_label = tk.Label(self.root, text="Status" if self.app_state.typing_active else "Typing: Stopped")
        self.status_label.configure(bg='darkgray')
        self.status_label.place(x=10, y=165, width=280, height=15)

        # Create a non-editable text box: status
        self.status_text_box = tk.Text(self.root,  height=10, width=40)
        self.print_status()
        self.status_text_box.config(state=tk.DISABLED)
        self.status_text_box.place(x=10, y=185, width=280, height=100)

        # Create Commands label
        self.commands_label = tk.Label(self.root, text="Commands")
        self.commands_label.configure(bg='darkgray')
        self.commands_label.place(x=10, y=290, width=280, height=15)

        # Create a button to toggle expand/collapse
        self.toggle_commands_button = tk.Button(self.root, text="Collapse", command=self.toggle_status_textbox)
        self.toggle_commands_button.place(x=10, y=290, width=80, height=15)

        # Create a non-editable text box: commands
        self.commands_text_box = tk.Text(self.root, height=10, width=40)
        self.print_all_commands(commands)
        self.commands_text_box.config(state=tk.DISABLED)
        self.commands_text_box.place(x=10, y=310, width=280, height=300)

        # Automatically adjust the window size to wrap content
        self.adjust_window_size()

        # Create the main window
        self.root.mainloop()

    def reload_commands(self):
        """Reload the commands from the updated commands file and display them in the UI."""
        # Clear the commands text box
        self.commands_text_box.commands(state=tk.NORMAL)
        self.commands_text_box.delete(1.0, tk.END)

        # Reload updated commands
        with open("commands.json", 'r') as f:
            commands = json.load(f)

        # Re-display the commands
        self.print_all_commands(commands)
        self.commands_text_box.commands(state=tk.DISABLED)

    def toggle_status_textbox(self):
        """Toggle between expanding and collapsing the Text widget."""
        if self.commands_text_box.winfo_height() == 300:
            self.commands_text_box.place(width=280, height=50)
            self.toggle_commands_button.commands(text="Expand")  # Change button text to Collapse
        else:
            self.commands_text_box.place(width=280, height=300) # Collapse the Text widget
            self.toggle_commands_button.commands(text="Collapse")  # Change button text to Expand

        # Adjust the window size after changing the widget
        self.adjust_window_size()

    def adjust_window_size(self) -> None:
        """Adjust window size based on widget sizes."""
        default_height = 300
        adjusted_height_1 = 310
        adjusted_height_2 = 620
        if self.commands_text_box.winfo_height() == default_height:
            required_height = adjusted_height_1
        else:
            required_height = adjusted_height_2
        self.root.update_idletasks()  # Make sure sizes are updated
        required_width = adjusted_height_1
        self.root.geometry(f"{required_width}x{required_height}")

    def on_terminate_button_click(self) -> None:
        """
        Set the termination flag to True, and destroy the main window.
        """
        self.app_state.terminate = True  # Signal all threads to terminate
        if hasattr(self, 'speech_thread') and self.speech_thread.is_alive():
          self.speech_thread.join()  # Wait for the thread to finish
        self.root.destroy()   # Close the UI

    def terminate_all_threads(self):
        """
        Safely terminates the speech thread and exits the main thread.
        """
        try:
            # Set the termination flag to stop the live interpreter
            self.app_state.terminate = True
            # Ensure the speech thread is joined (wait for it to finish)
            if hasattr(self, 'speech_thread') and self.speech_thread.is_alive():
                self.speech_thread.join()
            sys.exit(0)  # Terminate the main thread and exit the program
        except:
            pass

    def on_wake_up_button_click(self) -> None:
        """
        Activates the typing mode by setting 'typing_active' to True in the current state and updates the UI status.
        """
        self.app_state.typing_active = True
        self.app_state.print_status()

    def on_go_to_sleep_button_click(self) -> None:
        """
        Deactivates the typing mode by setting 'typing_active' to False in the current state and updates the UI status.
        """
        self.app_state.typing_active = False
        self.app_state.print_status()

    def print_all_commands(self, commands) -> None: # TODO: DISPLAY ONLY ACTIVE COMMANDS
        """
        Display the active commands in the user interface based on the provided commands.

        Parameters:
            commands: A dictionary containing the commands.

        Returns:
            None
        """
        for command_type in commands:
            self.commands_text_box.insert(tk.END, "┌────────────────────────────┐\n")
            self.commands_text_box.insert(tk.END, f"│ {command_type}:\n")
            self.commands_text_box.insert(tk.END, "├────────────────────────────┤\n")
            for command in commands[command_type]:
                for key, val in command.items():
                    if key == "name":
                        self.commands_text_box.insert(tk.END, f" {val}")
                self.commands_text_box.insert(tk.END, "\n")
            self.commands_text_box.insert(tk.END, "└────────────────────────────┘\n")

    def print_status(self) -> None:
        """
        Updates the UI to reflect the current status.
        """
        self.app_state.print_status()

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
        # self.status_text_box.see(tk.END)  # Scroll to the end
        self.status_text_box.config(state=tk.DISABLED)  # Disable editing again