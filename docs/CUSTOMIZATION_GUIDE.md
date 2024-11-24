# Customizing Texter

This guide provides instructions for customizing the Texter application to your preferences.

### Modifying speech commands

The files in `speech_commands` allows you to personalize the app's behavior. Here's how:

* **Keyboard Shortcuts:** Define voice commands to trigger specific keyboard shortcuts.
* **Info Commands:** Create commands that automatically type specific text strings.
* **Selection Commands:** Assign voice commands to perform text selection and editing actions.
* **Programming Language Commands:** Configure voice commands specific to a programming language for code typing and execution.

### Example json files:

`speech_commands/keyboard_commands.json`
```json
{
    "keyboard_commands": [
        {"name": "type 'hello'", "command_type": "keyboard", "key": "hello"},
        {"name": "press ctrl+c", "command_type": "keyboard", "key": "ctrl+c"}
    ]
}
```
`speech_commands/selection_commands.json`
```json
{
    "selection_commands": [
        {"name": "select line", "command_type": "selection"},
        {"name": "delete line", "command_type": "selection"}
    ],
    "python_commands": [
        {"name": "print hello", "command_type": "programming", "key": "print('hello')"}
    ]
}
```

