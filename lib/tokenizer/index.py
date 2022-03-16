from re import sub as re_sub, IGNORECASE, MULTILINE
from nltk.stem.porter import PorterStemmer


class Tokenizer:
    def __init__(self):
        self.stemmer = PorterStemmer()
        self.stemmerMap = {}

    @staticmethod
    def remove_noise(text="") -> str:
        if type(text) is not str:
            raise ValueError()

        return re_sub(r'([^A-Za-z\-\s]|\n+|\s+)', " ", text, flags=IGNORECASE | MULTILINE)

    @staticmethod
    def normalize(denoised_text="") -> str:
        """
        Normalization has been divided into 3 steps
        1) lowercase text
        2) replace consecutive \\s with single \\s
        3) trim/strip text
        :param denoised_text:
        :return:
        """

        if type(denoised_text) is not str:
            raise ValueError()

        trimmed_text = re_sub(r'\s+', " ", denoised_text.lower()).strip()
        return trimmed_text.encode('utf-8', 'ignore').decode('utf-8')

    @staticmethod
    def tokenize(normalized_text="") -> list:
        if type(normalized_text) is not str:
            raise ValueError()

        # split at whitespace
        return normalized_text.split(sep=" ")

    def stem(self, token):
        return self.stemmerMap[token] if token in self.stemmerMap else self.stemmer.stem(token)

    def get_terms(self, text="") -> list:
        """
        Stemmed terms are returned
        :param text:
        :return:
        """
        denoised_text = self.remove_noise(text)
        normalized_text = self.normalize(denoised_text)
        tokens = self.tokenize(normalized_text)

        print('Denoised', denoised_text)
        print('Normalized', normalized_text)
        print('Tokens', tokens)

        return list(
            map(lambda token: self.stemmerMap[token] if token in self.stemmerMap else self.stemmer.stem(token), tokens))
