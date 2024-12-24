import os
import unittest
from unittest.mock import patch, MagicMock
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))
from src.commands.text_processor import TextProcessor


class TestTextProcessor(unittest.TestCase):
    @patch("TextProcessor.pipeline")
    def setUp(self, mock_pipeline):
        # Set up mock pipeline and TextProcessor instance
        self.mock_pipe = MagicMock()
        mock_pipeline.return_value = self.mock_pipe
        self.text_processor = TextProcessor()

    def test_preprocess(self):
        # Test text preprocessing, ensuring punctuation is removed as expected
        text = "Hello, world! This is a test."
        expected_output = ["Hello", "world", "This", "is", "a", "test"]
        result = self.text_processor.preprocess(text)
        self.assertEqual(result, expected_output)

    def test_restore_punctuation(self):
        # Mock the predict and prediction_to_text methods
        with patch.object(
            self.text_processor,
            "predict",
            return_value=[["Hello", "0", 0.99], ["world", ".", 0.99]],
        ) as mock_predict, patch.object(
            self.text_processor, "prediction_to_text", return_value="Hello world."
        ):
            text = "Hello world"
            result = self.text_processor.restore_punctuation(text)
            self.assertEqual(result, "Hello world.")
            mock_predict.assert_called_once()

    def test_capitalize_sentences(self):
        # Test sentence capitalization
        text = "hello world. this is a test! can it work? yes."
        expected_output = "Hello world. This is a test! Can it work? Yes."
        result = self.text_processor.capitalize_sentences(text)
        self.assertEqual(expected_output, result)

    def test_overlap_chunks(self):
        # Test overlap_chunks method with sample data
        lst = list(range(10))
        n = 5
        stride = 2
        expected_output = [[0, 1, 2, 3, 4], [3, 4, 5, 6, 7], [6, 7, 8, 9]]
        result = list(self.text_processor.overlap_chunks(lst, n, stride))
        self.assertEqual(result, expected_output)

    def test_predict(self):
        # Mock pipe output and test predict method
        words = ["Hello", "world", "test"]
        mock_output = [
            {"end": 5, "entity": "0", "score": 0.9989766},  # "Hello"
            {"end": 11, "entity": ".", "score": 0.99827456},  # "world"
            {"end": 16, "entity": "0", "score": 0.0},  # "test"
        ]
        self.mock_pipe.return_value = mock_output
        result = self.text_processor.predict(words)
        expected_output = [
            ["Hello", "0", 0.9989766],
            ["world", ".", 0.99827456],
            ["test", "0", 0.0],
        ]
        self.assertEqual(
            len(result),
            len(expected_output),
            "Lengths of result and expected_output do not match",
        )

        for actual, expected in zip(result, expected_output):
            self.assertEqual(actual[0], expected[0], "Words do not match")
            self.assertEqual(actual[1], expected[1], "Entities do not match")
            self.assertAlmostEqual(
                actual[2], expected[2], places=5, msg="Scores do not match"
            )

    def test_prediction_to_text(self):
        # Test prediction to text conversion
        prediction = [["Hello", "0", 0.99], ["world", ".", 0.95], ["test", "0", 0.92]]
        expected_output = "Hello world. test"
        result = self.text_processor.prediction_to_text(prediction)
        self.assertEqual(result, expected_output)


if __name__ == "__main__":
    unittest.main()
