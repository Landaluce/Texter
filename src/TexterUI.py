# Standard library imports
import tkinter as tk


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
        self.root = tk.Tk()

        self.state = None
        self.commands_label = None
        self.input_text_box = None
        self.commands_text_box = None
        self.wake_up_button = None
        self.go_to_sleep_button = None
        self.terminate_button = None
        self.status_label = None
        self.status_text_box = None

    def init_ui(self, state, config):
        """
        Initializes the Texter user interface with input elements, buttons, and labels based on the provided state and configuration.

        Parameters:
        - state: The current state of the user interface.
        - config: The configuration settings for the user interface elements.

        Returns:
        None
        """
        # Create the main window
        # self.root = tk.Tk()

        self.root.protocol("WM_DELETE_WINDOW", self.disable_close)  # Override the close window button (X)
        self.root.title("Texter")  # Set the window title
        self.state = state

        # Set the dimensions and position of the window (width x height + x_offset + y_offset
        self.root.geometry("300x600+100+100")
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

        self.go_to_sleep_button = tk.Button(self.root, text="Go to Sleep", command=self.on_go_to_sleep_button_clik)
        self.go_to_sleep_button.place(x=110, y=130, width=100, height=30)

        self.terminate_button = tk.Button(self.root, text="Quit", command=self.on_terminate_button_click)
        self.terminate_button.place(x=210, y=130, width=80, height=30)

        # Create status label
        self.status_label = tk.Label(self.root, text="Status" if self.state.typing_active else "Typing: Stopped")
        self.status_label.configure(bg='darkgray')
        self.status_label.place(x=10, y=165, width=280, height=15)

        # Create a non-editable text box: status
        self.status_text_box = tk.Text(self.root, height=10, width=40)
        self.print_status()
        self.status_text_box.config(state=tk.DISABLED)
        self.status_text_box.place(x=10, y=185, width=280, height=100)

        # Create Commands label
        self.commands_label = tk.Label(self.root, text="Commands")
        self.commands_label.configure(bg='darkgray')
        self.commands_label.place(x=10, y=290, width=280, height=15)

        # Create a non-editable text box: commands
        self.commands_text_box = tk.Text(self.root, height=10, width=40)
        self.print_all_commands(config)
        self.commands_text_box.config(state=tk.DISABLED)
        self.commands_text_box.place(x=10, y=310, width=280, height=300)

        self.root.mainloop()

    def disable_close(self):
        """
        Closes the main window when the close button is clicked.
        """
        self.root.destroy()
        # return None  # Prevent the window from closing

    def on_terminate_button_click(self):
        """
        Set the termination flag to True, and destroy the main window.
        """
        self.state.terminate = True
        if hasattr(self, 'speech_thread'):
          self.speech_thread.join()  # Wait for the thread to finish
        self.root.destroy()

    def on_wake_up_button_click(self):
        """
        Activates the typing mode by setting 'typing_active' to True in the current state and updates the UI status.
        """
        self.state.typing_active = True
        self.state.print_status()

    def on_go_to_sleep_button_clik(self):
        """
        Deactivates the typing mode by setting 'typing_active' to False in the current state and updates the UI status.
        """
        self.state.typing_active = False
        self.state.print_status()

    def print_all_commands(self, config):  # DISPLAY ONLY ACTIVE COMMANDS
        """
        Display the active commands in the user interface based on the provided configuration.

        Parameters:
        - config: A dictionary containing the configuration settings for the commands.

        Returns:
        None
        """
        for command_type in config:
            self.commands_text_box.insert(tk.END, "┌────────────────────────────┐\n")
            self.commands_text_box.insert(tk.END, f"│ {command_type}:\n")
            self.commands_text_box.insert(tk.END, "├────────────────────────────┤\n")
            for command in config[command_type]:
                for key, val in command.items():
                    if key == "name":  # "command_type":
                        self.commands_text_box.insert(tk.END, f"│ {val}")
                self.commands_text_box.insert(tk.END, "\n")
            self.commands_text_box.insert(tk.END, "└────────────────────────────┘\n")

    def print_status(self):
        """
        Updates the UI to reflect the current status.
        """
        self.state.print_status(self)

    def append_text(self, text):
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

    def update_status(self, status_message):
        """
        Thread-safe update to the status_text_box.
        """
        self.root.after(0, self._update_status_ui, status_message)

    def _update_status_ui(self, status_message):
        """
        Updates the status_text_box with the latest status message.
        """
        self.status_text_box.config(state=tk.NORMAL)  # Enable editing to insert text
        self.status_text_box.delete(1.0, tk.END)  # Clear the current content
        self.status_text_box.insert(tk.END, status_message)  # Insert new status
        self.status_text_box.see(tk.END)  # Scroll to the end
        self.status_text_box.config(state=tk.DISABLED)  # Disable editing again