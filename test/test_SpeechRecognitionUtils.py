import unittest
from unittest.mock import patch, MagicMock
import speech_recognition as sr
from src.SpeechRecognitionUtils import recognize_speech, live_speech_interpreter


class TestSpeechRecognitionUtils(unittest.TestCase):

    @patch('speech_recognition.Recognizer.listen')
    @patch('speech_recognition.Recognizer.recognize_google')
    def test_recognize_speech_success(self, mock_recognize_google, mock_listen):
        mock_audio = MagicMock()
        mock_listen.return_value = mock_audio
        mock_recognize_google.return_value = "hello world"
        recognizer = sr.Recognizer()

        result = recognize_speech(recognizer)
        self.assertEqual(result, "hello world")

    @patch('speech_recognition.Recognizer.listen')
    @patch('speech_recognition.Recognizer.recognize_google')
    def test_recognize_speech_failure(self, mock_recognize_google, mock_listen):
        mock_listen.side_effect = sr.UnknownValueError
        recognizer = sr.Recognizer()

        result = recognize_speech(recognizer)
        self.assertIsNone(result)

    # TODO: fix this test
    # @patch('src.SpeechRecognitionUtils.recognize_speech')
    # def test_live_speech_interpreter(self, mock_recognize_speech):
    #     mock_recognize_speech.return_value = "switch mode"
    #     app_state = MagicMock()
    #     texter_ui = MagicMock()
    #     recognizer = MagicMock()
    #
    #     live_speech_interpreter(app_state, texter_ui, recognizer)
    #     app_state.switch_mode.assert_called_once()


if __name__ == '__main__':
    unittest.main()