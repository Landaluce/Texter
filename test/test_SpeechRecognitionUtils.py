import unittest
from unittest.mock import patch, MagicMock
import speech_recognition as sr
from src.utils.speech_recognition import recognize_speech
from src.utils.live_speech_interpreter import live_speech_interpreter


class TestSpeechRecognitionUtils(unittest.TestCase):

    @patch("speech_recognition.Recognizer.listen")
    @patch("speech_recognition.Recognizer.recognize_google")
    def test_recognize_speech_success(self, mock_recognize_google, mock_listen):
        mock_audio = MagicMock()
        mock_listen.return_value = mock_audio
        mock_recognize_google.return_value = "hello world"
        recognizer = sr.Recognizer()

        result = recognize_speech(recognizer)
        self.assertEqual(result, "hello world")

    @patch("speech_recognition.Recognizer.listen")
    @patch("speech_recognition.Recognizer.recognize_google")
    def test_recognize_speech_failure(self, mock_recognize_google, mock_listen):
        mock_listen.side_effect = sr.UnknownValueError
        recognizer = sr.Recognizer()

        result = recognize_speech(recognizer)
        self.assertIsNone(result)

    # TODO: fix this
    @patch("src.SpeechRecognitionUtils.recognize_speech")
    def test_live_speech_interpreter(self, mock_recognize_speech):
        mock_recognize_speech.return_value = "switch mode"

        # Mock app_state and its methods
        app_state = MagicMock()
        app_state.terminate = False  # Start with the loop enabled
        app_state.print_status = MagicMock()  # Avoid actual print calls

        # Mock texter_ui and its methods
        texter_ui = MagicMock()
        texter_ui.print_status = MagicMock()  # Avoid actual print calls
        texter_ui.append_text = MagicMock()  # Avoid actual append calls

        recognizer = MagicMock()

        # Run the live_speech_interpreter function in a modified way for testing
        def testable_interpreter():
            app_state.terminate = True  # Ensure we exit after one iteration
            live_speech_interpreter(app_state, texter_ui, recognizer)

        # Run the function
        testable_interpreter()

        # Verify if switch_mode was called once
        app_state.switch_mode.assert_called_once()


if __name__ == "__main__":
    unittest.main()
