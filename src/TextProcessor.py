from transformers import pipeline
import re
import torch


class TextProcessor:
    def __init__(self, model="oliverguhr/fullstop-punctuation-multilang-large") -> None:
        if torch.cuda.is_available():
            self.pipe = pipeline("ner", model, grouped_entities=False, device=0)
        else:
            self.pipe = pipeline("ner", model, grouped_entities=False)

    @staticmethod
    def preprocess(text):
        acronyms = re.findall(r"(?:\b[A-Z]\.){2,}\b", text)  # Find all acronyms
        text = re.sub(r"(?<!\d)[.,;:!?](?!\d)", "", text)  # Remove other punctuation

        # Reinsert acronyms if they were modified
        for acronym in acronyms:
            text = text.replace(acronym.replace(".", ""), acronym)

        text = text.split()
        return text

    def restore_punctuation(self, text):
        if not text.strip():
            return ""
        result = self.predict(self.preprocess(text))
        return self.prediction_to_text(result)

    @staticmethod
    def capitalize_sentences(text):
        text = re.sub(r"(?<=[.!?]) +", "##SPLIT##", text)  # Split sentences
        sentences = text.split("##SPLIT##")

        # Capitalize the first character of each sentence
        sentences = [sentence.strip().capitalize() for sentence in sentences]

        # Reassemble the text with proper sentence endings
        return " ".join(sentences)
        # TODO detect: I,  I'm, I'll, I've, I'd

    @staticmethod
    def overlap_chunks(lst, n, stride=0):
        """Yield successive n-sized chunks from lst with stride length of overlap."""
        for i in range(0, len(lst), n - stride):
            yield lst[i : i + n]
            if i + n >= len(lst):
                break

    def predict(self, words, chunk_size=230, overlap=5):
        if len(words) <= chunk_size:
            overlap = 0

        batches = list(self.overlap_chunks(words, chunk_size, overlap))

        tagged_words = []
        for batch in batches:
            text = " ".join(batch)
            result = self.pipe(text)

            # We now keep track of where we are in the result
            char_index = 0
            result_index = 0
            for word in batch:
                # Update char_index for the word
                char_index += len(word) + 1  # Account for the space after each word

                # Determine the appropriate label and score
                while (
                    result_index < len(result)
                    and char_index > result[result_index]["end"]
                ):
                    result_index += 1

                # Default label to "0" and score to None
                label = "0"
                score = 0.0

                # If within bounds, get the label and score from the result
                if result_index < len(result):
                    label = result[result_index]["entity"]
                    score = result[result_index]["score"]

                tagged_words.append([word, label, score])

        assert len(tagged_words) == len(words)
        return tagged_words

    @staticmethod
    def prediction_to_text(prediction):
        result = ""
        for word, label, _ in prediction:
            result += word
            if label == "0":
                result += " "
            if label in ".,?-:":
                result += label + " "
        return result.strip()
