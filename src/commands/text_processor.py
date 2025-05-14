"""
This module defines the `TextProcessor` class, which provides methods for processing text, including
restoring punctuation, capitalizing sentences, and handling overlapping chunks for predictions.
It uses a model from Hugging Face's pipeline to perform text restoration and utilizes chunking
and overlap techniques to handle long inputs efficiently.

Key Features:
1. **Text Preprocessing**: Cleans input text by removing unnecessary punctuation while preserving acronyms.
2. **Punctuation Restoration**: Restores punctuation to text that has been stripped of punctuation marks.
3. **Sentence Capitalization**: Capitalizes the first letter of each sentence in the given text.
4. **Chunking and Overlap**: Processes long texts by breaking them into smaller chunks with overlapping words.
5. **Prediction Alignment**: Aligns predictions with the original text and restores punctuation, taking confidence scores into account.

Classes:
- `TextProcessor`: The main class for text processing that provides methods for punctuation restoration,
  sentence capitalization, and handling predictions with chunking and overlap.

Methods:
- `__init__(self, model="oliverguhr/fullstop-punctuation-multilang-large", chunk_size=230, overlap=5)`:
   Initializes the `TextProcessor` with a specific Hugging Face model and settings for chunking and overlap.

- `preprocess(text)`:
   Removes unnecessary punctuation and preserves acronyms in the input text.

- `restore_punctuation(self, text)`:
   Restores punctuation to text based on model predictions.

- `capitalize_sentences(text)`:
   Capitalizes the first letter of each sentence in the input text.

- `_predict(self, words)`:
   Processes input words by performing predictions using chunking and overlap.

- `_generate_chunks(self, words)`:
   Generates overlapping chunks of words for prediction.

- `_align_predictions(words, results, confidence_threshold=0.8)`:
   Aligns the model predictions with the input words, merging subword tokens and filtering based on confidence scores.

- `_prediction_to_text(predictions)`:
   Converts aligned predictions into a text string with restored punctuation.

Dependencies:
- `re`: Regular expression library for text processing.
- `transformers`: Hugging Face's library for working with pre-trained models.

Usage Example:
    text_processor = TextProcessor()
    text_with_punctuation = text_processor.restore_punctuation("this is a test sentence without punctuation")
    capitalized_text = text_processor.capitalize_sentences(text_with_punctuation)
"""
import re
from transformers import pipeline
import warnings
warnings.filterwarnings("ignore", message="`grouped_entities` is deprecated")


class TextProcessor:
    """
    A class for processing text, including punctuation restoration, sentence capitalization,
    and handling overlapping chunks for predictions.
    """

    def __init__(self, model="distilbert-base-uncased-finetuned-sst-2-english", chunk_size=230, overlap=5):
        """
        Initialize the TextProcessor with a specific model and settings.

        Args:
            model (str): The name of the Hugging Face model to use.
            chunk_size (int): Maximum number of words per chunk for processing.
            overlap (int): Number of overlapping words between consecutive chunks.
        """
        self.chunk_size = chunk_size
        self.overlap = overlap
        self.pipe = self._initialize_pipeline(model)

    @staticmethod
    def _initialize_pipeline(model):
        """Initialize the Hugging Face pipeline."""
        return pipeline("ner", model=model, grouped_entities=False, device=-1)

    @staticmethod
    def preprocess(text):
        """
        Preprocess the input text by removing unnecessary punctuation and preserving acronyms.

        Args:
            text (str): The input text to preprocess.

        Returns:
            list: A list of words after preprocessing.
        """
        acronyms = re.findall(r"(?:\b[A-Z]\.){2,}\b", text)  # Find acronyms
        text = re.sub(r"(?<!\d)[.,;:!?](?!\d)", "", text)  # Remove punctuation except within numbers

        # Restore acronyms if altered
        for acronym in acronyms:
            text = text.replace(acronym.replace(".", ""), acronym)

        return text.split()

    def restore_punctuation(self, text):
        """
        Restore punctuation to a given text.

        Args:
            text (str): The input text without proper punctuation.

        Returns:
            str: The text with restored punctuation.
        """
        if not text.strip():
            return ""

        words = self.preprocess(text)
        predictions = self._predict(words)
        return self._prediction_to_text(predictions)

    @staticmethod
    def capitalize_sentences(text):
        """
        Capitalizes the first letter of each sentence in the text.

        Args:
            text (str): The input text with sentences.

        Returns:
            str: The text with properly capitalized sentences.
        """
        sentences = re.split(r'([.!?])\s*', text)
        sentences = [sentence.capitalize() for sentence in sentences if sentence.strip()]
        return "".join(sentences)

    def _predict(self, words):
        """
        Perform predictions on the input words with optional chunking and overlap.

        Args:
            words (list): The list of words to process.

        Returns:
            list: A list of tagged words with their labels and scores.
        """
        chunks = list(self._generate_chunks(words))
        tagged_words = []

        for chunk in chunks:
            text = " ".join(chunk)
            results = self.pipe(text)
            tagged_words.extend(self._align_predictions(chunk, results))

        return tagged_words

    def _generate_chunks(self, words):
        """
        Generate overlapping chunks from the input word list.

        Args:
            words (list): The list of words to chunk.

        Yields:
            list: Chunks of words with the specified overlap.
        """
        step = self.chunk_size - self.overlap
        for i in range(0, len(words), step):
            yield words[i : i + self.chunk_size]
            if i + self.chunk_size >= len(words):
                break

    @staticmethod
    def _align_predictions(words, results, confidence_threshold=0.8):
        """
        Aligns predictions from the model with the input words,
        merging subword tokens to their corresponding word.

        Args:
            words (list): List of original words.
            results (list): List of token-level predictions.
            confidence_threshold (float): Minimum score to consider a label valid.

        Returns:
            list: Aligned predictions at the word level.
        """
        aligned = []
        result_index = 0

        for word in words:
            label = "0"  # Default label
            max_score = 0.0

            while result_index < len(results) and results[result_index]["word"].startswith("▁"):
                token = results[result_index]
                if token["score"] > confidence_threshold:
                    label = token["entity"]  # Assign label with confidence
                    max_score = max(max_score, token["score"])
                result_index += 1

            aligned.append((word, label, max_score))

        return aligned

    @staticmethod
    def _prediction_to_text(predictions):
        """
        Converts aligned predictions into punctuated text.

        Args:
            predictions (list): Aligned predictions (word, label, score).

        Returns:
            str: The punctuated text.
        """
        result = []
        for i, (word, label, _) in enumerate(predictions):
            if label in ".,?-:" and (i == len(predictions) - 1 or predictions[i + 1][1] == "0"):
                result.append(f"{word}{label}")  # Append punctuation directly to the word
            else:
                result.append(word)  # No punctuation
        return " ".join(result)
