class HybridIndex:
    """
    Merges InvertedIndex With Positional Indexes
    """
    def __init__(self):
        self.term_count = 0
        self.index = {}

        # term -> docFreq, PostingList, PositionalIndexes
        """
            Index[term] = [
                [docFreq],
                {
                    docID1: [posIndex1, posIndex2, ...]
                    docID2: [posIndex1, ...]
                    ...
                }
            ]
        """

    def get_postings_dict(self, term=None):
        if type(term) is not str:
            raise ValueError()

        # fail gracefully
        if term not in self.index:
            return {}

        return self.index[term][1]

    def get_postings_list(self, term=None):
        return sorted(self.get_postings_dict(term).keys())

    def get_positions(self, term=None, docID=None):
        if type(docID) is not int:
            raise ValueError()

        return self.get_postings_dict(term)[docID]

    def increment_doc_freq(self, term=None):
        if type(term) is not str:
            raise ValueError()

        if term in self.index:
            self.index[term][0] += 1

    def get_doc_freq(self, term=None):
        if type(term) is not str:
            raise ValueError()

        if term not in self.index:
            return 0

        return self.index[term][0]

    def add_posting(self, term=None, docID=None, position=None):
        if type(term) is not str or type(docID) is not int or position is None:
            raise ValueError()

        if term not in self.index:
            self.term_count += 1
            self.index[term] = [0, {}]

        postings_dict = self.get_postings_dict(term)

        if docID not in postings_dict:
            postings_dict[docID] = []

        self.increment_doc_freq(term)
        postings_dict[docID].append(position)
