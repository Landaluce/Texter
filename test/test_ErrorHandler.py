import unittest
from unittest.mock import patch, MagicMock
import sys
sys.path.append('/home/alvaro/Desktop/Texter/src/')
from src.ErrorHandler import noalsaerr, c_error_handler

# TODO: fix this
class TestErrorHandler(unittest.TestCase):
    @patch("ErrorHandler.cdll")
    def test_noalsaerr_context_manager(self, mock_cdll):
        # Mock the behavior of cdll.LoadLibrary
        mock_a_sound = MagicMock()
        mock_cdll.LoadLibrary.return_value = mock_a_sound

        with noalsaerr():
            # Check that snd_lib_error_set_handler is called
            mock_a_sound.snd_lib_error_set_handler.assert_called_once_with(c_error_handler)

        # Check that snd_lib_error_set_handler is unset
        mock_a_sound.snd_lib_error_set_handler.assert_called_with(None)

    @patch("ErrorHandler.cdll.LoadLibrary")
    def test_noalsaerr_library_load_failure(self, mock_load_library):
        """
        Test the behavior when libasound cannot be loaded.
        """
        mock_load_library.side_effect = OSError("Library not found")

        with self.assertRaises(OSError) as context:
            with noalsaerr():
                pass  # The context manager should raise the error if the library is missing.

        self.assertIn("Library not found", str(context.exception))


if __name__ == "__main__":
    unittest.main()
