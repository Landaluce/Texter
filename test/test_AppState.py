import sys
import unittest
from unittest.mock import patch

from src.state.app_state import AppState, CommandType, CommandManager


class TestAppState(unittest.TestCase):

    def setUp(self):
        self.app_state = AppState()

    def test_initialization(self):
        """Test that AppState initializes with correct default values."""
        self.assertEqual(self.app_state.mode, "dictation")
        self.assertFalse(self.app_state.spelling)
        self.assertTrue(self.app_state.typing_active)
        self.assertEqual(self.app_state.programming_language, "python")
        self.assertEqual(self.app_state.terminal_os, "linux")

    def test_load_commands(self):
        """Test loading various commands into AppState."""
        commands = {
            "keyboard_commands": [
                {
                    "name": "test_keyboard",
                    "command_type": "keyboard",
                    "key": "k",
                    "num_key": "test_keyboard",
                },
                {"name": "stop", "command_type": "start_stop", "num_key": "stop"},
            ],
            "info_commands": [{"name": "show info", "key": "i"}],
            "selection_commands": [{"name": "select all"}],
            "python_commands": [{"name": "print statement", "key": "print()"}],
            "linux_commands": [{"name": "ls", "key": "ls"}],
            "spelling_commands": [{"name": "alpha", "key": "a"}],
            "git_commands": [{"name": "git status", "key": "status"}],
        }
        self.app_state.load_commands(commands)

        # Verify commands loaded into appropriate attributes
        self.assertEqual(len(self.app_state.keyboard_commands), 2)
        self.assertEqual(len(self.app_state.info_commands), 1)
        self.assertEqual(len(self.app_state.selection_commands), 1)
        self.assertEqual(len(self.app_state.programming_commands), 1)
        self.assertEqual(len(self.app_state.terminal_commands), 1)
        self.assertEqual(len(self.app_state.spelling_commands), 1)
        self.assertEqual(len(self.app_state.git_commands), 1)

    @patch("pyautogui.hotkey")
    def test_handle_keyboard_command(self, mock_write):
        """Test handling of keyboard commands."""
        self.app_state.keyboard_commands = [
            CommandManager("test_keyboard", CommandType.KEYBOARD, "k", "test_keyboard")
        ]
        handled = self.app_state._handle_keyboard_command("test_keyboard")

        self.assertTrue(handled)
        mock_write.assert_called_once_with("k")

    @patch("pyautogui.write")
    def test_handle_programming_command(self, mock_write):
        """Test handling of programming commands."""
        self.app_state.programming_commands = [
            CommandManager("print statement", CommandType.PROGRAMMING, "==print()==")
        ]
        handled = self.app_state._handle_programming_command("print statement")
        self.assertTrue(handled)
        mock_write.assert_called_with("==print()==")

    # TODO: fix this
    @patch("pyautogui.write")
    def test_handle_terminal_command(self, mock_write):
        """Test handling of terminal commands."""
        self.app_state.terminal_commands = [CommandManager("ls", CommandType.TERMINAL, "ls")]
        handled = self.app_state._handle_terminal_command("ls")
        self.assertTrue(handled)
        mock_write.assert_called_with("ls")

    @patch("pyautogui.write")
    def test_handle_spelling_command(self, mock_write):
        """Test handling of spelling commands."""
        self.app_state.spelling_commands = [CommandManager("alpha", CommandType.SPELLING, "a")]
        handled = self.app_state._handle_spelling_command("alpha")
        self.assertTrue(handled)
        mock_write.assert_called_with("a")

    def test_switch_mode(self):
        """Test switching between dictation and spelling modes."""
        self.assertEqual(self.app_state.mode, "dictation")
        self.app_state.switch_mode()
        self.assertEqual(self.app_state.mode, "spelling")
        self.app_state.switch_mode()
        self.assertEqual(self.app_state.mode, "dictation")

    @patch("builtins.print")
    def test_print_status(self, mock_print):
        """Test that print_status outputs correct application status."""
        self.app_state.update_status()
        mock_print.assert_called_once_with(
            "Typing: started\n"
            "mode: dictation\n"
            "python Programming: On\n"
            "linux Terminal: On\n"
            "Punctuation: Off | Caps: Off\n"
        )

    @patch("sys.exit")
    @patch("subprocess.Popen")
    def test_restart_script(self, mock_popen, mock_exit):
        """Test that restart_script restarts the script."""
        self.app_state.restart_script()
        mock_popen.assert_called_once_with([sys.executable, sys.argv[0]])
        mock_exit.assert_called_once()


if __name__ == "__main__":
    unittest.main()
