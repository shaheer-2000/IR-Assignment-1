from lib.fs_manager import FSM
from lib.data_structures import HybridIndex
from lib.tokenizer import Tokenizer
from lib.utility import Utils

class IndexBuilder:
    def __init__(self):
        self.tokenizer = Tokenizer()
        self.stopwords = []
        self.index = HybridIndex()

    def get_stopwords(self, stopwords_path):
        try:
            self.stopwords = FSM.read_file(stopwords_path).strip().split('\n')
        except Exception:
            self.stopwords = []

    def is_stopword(self, term):
        return term in self.stopwords

    def build_index(self, collection_path: str, stopwords_path: str, pickle_path = None):
        if type(pickle_path) is str:
            try:
                self.index = FSM.unpickle_struct(pickle_path)
                return
            except Exception:
                print("Pickled index does not exist, creating new index")

        docs = Utils.sort_and_stringify(
            FSM.get_files_in_dir(collection_path, lambda f: int(f[:-4])))

        self.get_stopwords(stopwords_path)

        for doc in docs:
            content = FSM.read_file(FSM.resolve_path(f'{collection_path}/{doc}.txt'))
            print(doc, content)
            terms = self.tokenizer.get_terms(content)

            for index, term in enumerate(terms):
                if self.is_stopword(term):
                    continue

                self.index.add_posting(term, int(doc), index)

        FSM.pickle_struct(pickle_path, self.index)