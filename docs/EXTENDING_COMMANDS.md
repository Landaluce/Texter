# Extending Texter's Commands

This guide details how to add new command types to the Texter application.

### Adding a New Command Type

Here's a step-by-step guide to extend the app's functionality:

1. **Modify or add json files in the`speech_commands`directory:**
   * Define your new command type in the appropriate section (e.g., `keyboard_commands`, `info_commands`, `selection_commands`).
   * Specify the command's name, key (if applicable), and any other relevant properties.

2. **Update `CommandType` in `CommandClasses.py`:**
   * Add a new enum value to `CommandType` to represent the new command type.

3. **Modify `Command` in `CommandClasses.py`:**
   * Create a new method, `_execute_new_command_type(text)`, to handle the execution of the new command type.
   * Implement the logic for the new command within this method.

4. **Update `AppState` in `AppState.py`:**
   * Modify the `load_commands` method to include the new command type in the loaded commands.
   * Create a new method, `_handle_new_command(text)`, to check if the recognized text matches any of the new commands.
   * Implement the logic for handling the new command within this method.

5. **Add new commands to `get_active_commands` in `TexterUI` so they are listed in the UI (Optional)

### Example

Suppose you want to add a new command type for controlling media playback:

**Steps:**

1. Crete `media_control_commands.json` in `speech_commands`
2. Define media-related commands in this file.
3. Update `CommandType` in `CommandClasses.py` with a new enum value for "MEDIA".
4. Create a new method in `Command` to handle media playback commands.
5. Update `AppState.py` to load and handle media commands.

**Refer to the codebase for a detailed implementation examples.**

### Additional Considerations:

* Implement error handling for unexpected situations.
* Thoroughly test your new command type.
* Update the project's documentation to reflect the new functionality.

By following these steps, you can effectively extend Texter's capabilities!
