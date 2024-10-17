from concurrent.futures import process
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
        # remove markers except for markers in numbers
        text = re.sub(r"(?<!\d)[.,;:!?](?!\d)", "", text)
        # todo: match acronyms https://stackoverflow.com/questions/35076016/regex-to-match-acronyms
        text = text.split()
        return text

    def restore_punctuation(self, text):
        result = self.predict(self.preprocess(text))
        return self.prediction_to_text(result)

    @staticmethod
    def capitalize_sentences(text):
        # List of sentence-ending punctuation
        sentence_ending_punctuations = ['? ', '. ', '! ']

        # Iterate over each punctuation mark and capitalize accordingly
        for punctuation in sentence_ending_punctuations:
            if punctuation in text:
                sentences = text.split(punctuation)
                sentences = [sentence.capitalize() for sentence in sentences]
                text = punctuation.join(sentences)  # Reassemble the text with the current punctuation


        # I
        # I'm
        # I'll
        # I've
        # I'd
        return text

    @staticmethod
    def overlap_chunks(lst, n, stride=0):
        """Yield successive n-sized chunks from lst with stride length of overlap."""
        for i in range(0, len(lst), n - stride):
            yield lst[i:i + n]

    def predict(self, words):
        overlap = 5
        chunk_size = 230
        if len(words) <= chunk_size:
            overlap = 0

        batches = list(self.overlap_chunks(words, chunk_size, overlap))

        # if the last batch is smaller than the overlap,
        # we can just remove it
        if len(batches[-1]) <= overlap:
            batches.pop()

        tagged_words = []
        for batch in batches:
            # use last batch completely
            if batch == batches[-1]:
                overlap = 0
            text = " ".join(batch)
            result = self.pipe(text)
            assert len(text) == result[-1]["end"], "chunk size too large, text got clipped"

            char_index = 0
            result_index = 0
            for word in batch[:len(batch) - overlap]:
                char_index += len(word) + 1
                # if any sub-token of a word is labeled as sentence end
                # we label the whole word as sentence end
                label = 0
                while result_index < len(result) and char_index > result[result_index]["end"]:
                    label = result[result_index]['entity']
                    score = result[result_index]['score']
                    result_index += 1

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