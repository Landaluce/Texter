# Customizing Texter

This guide provides instructions for customizing the Texter application to your preferences.

### Modifying `config.json`

The `config.json` file allows you to personalize the app's behavior. Here's how:

* **Keyboard Shortcuts:** Define voice commands to trigger specific keyboard shortcuts.
* **Info Commands:** Create commands that automatically type specific text strings.
* **Selection Commands:** Assign voice commands to perform text selection and editing actions.
* **Programming Language Commands:** (Optional) Configure voice commands specific to a programming language for code typing and execution.

### Example Configuration:

```json
{
    "keyboard_commands": [
        {"name": "type 'hello'", "command_type": "keyboard", "key": "hello"},
        {"name": "press ctrl+c", "command_type": "keyboard", "key": "ctrl+c"}
    ],
    "info_commands": [
        {"name": "type my email", "command_type": "info", "key": "[email address removed]"}
    ],
    "selection_commands": [
        {"name": "select line", "command_type": "selection"},
        {"name": "delete line", "command_type": "selection"}
    ],
    "python_commands": [
        {"name": "print hello", "command_type": "programming", "key": "print('hello')"}
    ]
}
