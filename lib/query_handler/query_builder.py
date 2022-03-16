from lib.fs_manager import FSM
from lib.tokenizer import Tokenizer


class TokenType:
    AND, OR, NOT, QUERY_TERM, PROXIMITY = range(5)


class Token:
    def __init__(self, token):
        self.token = token
        self.token_type = Token.get_token_type(token)
        self.next_token = None

    @staticmethod
    def get_token_type(token):
        if token == "AND":
            return TokenType.AND
        elif token == "OR":
            return TokenType.OR
        elif token == "NOT":
            return TokenType.NOT
        elif token.startswith("/"):
            return TokenType.PROXIMITY
        else:
            return TokenType.QUERY_TERM


class QueryBuilder:
    def __init__(self):
        self.tokenizer = Tokenizer()
        self.stopwords = []

    def get_stopwords(self, stopwords_path):
        try:
            self.stopwords = FSM.read_file(stopwords_path).strip().split('\n')
        except Exception:
            self.stopwords = []

    def is_stopword(self, term):
        return term in self.stopwords

    def tokenize_query(self, query):
        filtered_tokens = list(map(lambda t: self.tokenizer.stem(t) if t not in ["AND", "OR", "NOT"] and not t.startswith("/") else t, query.strip().split(" ")))
        # filtered_tokens = list(filter(self.is_stopword, self.tokenizer.get_terms(query)))
        query_tokens = []
        token_count = len(filtered_tokens)

        i = 0
        while i < token_count:
            if i != 0:
                token = Token(filtered_tokens[i])
                query_tokens[i - 1].next_token = token
                query_tokens.append(token)
            else:
                query_tokens.append(Token(filtered_tokens[i]))
            i += 1

        return query_tokens
