import unittest
from unittest.mock import patch, Mock, call

from src.CommandClasses import Command, CommandType


class TestCommandClasses(unittest.TestCase):
    def setUp(self):
        self.mock_app_state = Mock()
        self.mock_app_state.programming_language = "python"
        self.mock_app_state.terminal_os = "linux"

        self.command = Command(
            name="print statement",
            command_type=CommandType.PROGRAMMING,
            key="print statement",
        )

        self.spelling_commands = [
            Mock(name="alpha", key="a"),
            Mock(name="bravo", key="b"),
            Mock(name="charlie", key="c"),
        ]

    @patch("pyautogui.write")
    @patch("pyautogui.hotkey")
    def test_execute_keyboard_command(self, mock_hotkey, mock_write):
        self.command.key = "test_key"
        self.command.command_type = CommandType.KEYBOARD
        self.command.num_key = ""

        self.command.execute("print statement", self.mock_app_state)
        mock_hotkey.assert_called_with("test_key")
        self.assertEqual(mock_hotkey.call_count, 1)

    @patch("pyautogui.write")
    def test_execute_programming_command_python(self, mock_write):
        self.command.command_type = CommandType.PROGRAMMING
        self.command.execute("print statement", self.mock_app_state)
        mock_write.assert_called_with("print()")
        mock_write.assert_called_once()

    # TODO: fix this
    @patch("pyautogui.write")
    def test_execute_spelling_command(self, mock_write):
        # Set up the test scenario
        self.command.key = "alpha"
        self.command.command_type = CommandType.SPELLING
        self.command.num_key = "alpha"
        expected_output = "a"  # Replace with the actual expected output

        # Execute the command
        self.command.execute_spelling_command(self.mock_app_state, "alpha")

        # Assertions
        mock_write.assert_has_calls([
            call("alpha")
        ])
        mock_write.assert_called_with(expected_output)  # Ensure the last call is the expected output
        self.mock_app_state.append_text.assert_not_called()

    def test_extract_num(self):
        self.assertEqual(self.command._extract_num("five"), 5)
        self.assertEqual(self.command._extract_num("ten"), 10)
        self.assertEqual(self.command._extract_num("invalid"), 1)


if __name__ == "__main__":
    unittest.main()
