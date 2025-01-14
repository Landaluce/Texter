import re
import torch
from transformers import pipeline


class TextProcessor:
    """
    A class for processing text, including punctuation restoration, sentence capitalization,
    and handling overlapping chunks for predictions.
    """

    def __init__(self, model="oliverguhr/fullstop-punctuation-multilang-large", chunk_size=230, overlap=5):
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
        device = 0 if torch.cuda.is_available() else -1
        return pipeline("ner", model=model, grouped_entities=False, device=device)

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
        Capitalize the first letter of each sentence in the text.

        Args:
            text (str): The input text with sentences.

        Returns:
            str: The text with properly capitalized sentences.
        """
        text = re.sub(r"(?<=[.!?]) +", "##SPLIT##", text)  # Mark sentence boundaries
        sentences = text.split("##SPLIT##")
        sentences = [sentence.strip().capitalize() for sentence in sentences]
        return " ".join(sentences)

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
    def _align_predictions(chunk, results):
        """
        Align predictions from the model with the input chunk.

        Args:
            chunk (list): The current chunk of words.
            results (list): The model's predictions for the chunk.

        Returns:
            list: Aligned words with their labels and scores.
        """
        tagged = []
        result_index = 0
        char_index = 0

        for word in chunk:
            char_index += len(word) + 1  # Account for the space after each word

            # Find the corresponding prediction
            while result_index < len(results) and char_index > results[result_index]["end"]:
                result_index += 1

            # Default values if no prediction matches
            label = "0"
            score = 0.0

            if result_index < len(results):
                label = results[result_index]["entity"]
                score = results[result_index]["score"]

            tagged.append((word, label, score))

        return tagged

    @staticmethod
    def _prediction_to_text(predictions):
        """
        Convert predictions into a punctuated text.

        Args:
            predictions (list): List of tuples (word, label, score).

        Returns:
            str: The text with restored punctuation.
        """
        result = ""
        for word, label, _ in predictions:
            result += word
            if label == "0":
                result += " "
            elif label in ".,?-:":
                result += label + " "
        return result.strip()
