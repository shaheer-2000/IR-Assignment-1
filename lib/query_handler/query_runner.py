from lib.query_handler import QueryBuilder, TokenType
from lib.utility import Utils


class QueryRunner:
    def __init__(self, index):
        self.index = index
        self.builder = QueryBuilder()

    def run_query(self, query):
        query_terms = self.builder.tokenize_query(query)

        res = None
        i = 0

        while i < len(query_terms):
            term = query_terms[i]

            if term.token_type == TokenType.NOT:
                res = Utils.diff_num_iterables(range(1, 449), self.index.get_postings_list(term.next_token.token))
                i += 2
            elif term.token_type == TokenType.AND:
                res = Utils.intersect_num_iterables(res, self.index.get_postings_list(term.next_token.token))
                i += 2
            elif term.token_type == TokenType.OR:
                res = Utils.union_num_iterables(res, self.index.get_postings_list(term.next_token.token))
                i += 2
            else:
                res = self.index.get_postings_list(term.token)
                if (i + 1) < len(query_terms) and term.next_token.token_type != TokenType.NOT and term.next_token.token_type != TokenType.AND and term.next_token.token_type != TokenType.OR:
                    proximity_terms = []
                    while (i < len(query_terms) and not query_terms[i].token.startswith("/")):
                        proximity_terms.append(query_terms[i].token)
                        i += 1

                    proximity_upper_bound = int(query_terms[i].token[1:]) + 1
                    proximity_iterator = 0

                    while proximity_iterator < len(proximity_terms):
                        proximity_postings_list = self.intersect_postings_by_position(proximity_terms[proximity_iterator], proximity_terms[proximity_iterator + 1], proximity_upper_bound)
                        # print(proximity_terms[proximity_iterator], proximity_terms[proximity_iterator + 1], proximity_upper_bound)
                        proximity_iterator += 2
                        if res is None:
                            res = proximity_postings_list
                        else:
                            res = Utils.intersect_num_iterables(res, proximity_postings_list)
                i += 1

        return res

    def intersect_postings_by_position(self, term_a: str, term_b: str, proximity_upper_bound):
        res = []

        # intersect both postings by docID first
        postings_list_a = self.index.get_postings_list(term_a)
        postings_list_b = self.index.get_postings_list(term_b)
        intersected_postings = Utils.intersect_num_iterables(postings_list_a, postings_list_b)

        # then use docID to search for positional criteria
        for docID in intersected_postings:
            positions_a = self.index.get_positions(term_a, docID)
            positions_b = self.index.get_positions(term_b, docID)

            count_positions_a = len(positions_a)
            count_positions_b = len(positions_b)

            i = 0
            j = 0

            while i <  count_positions_a and j < count_positions_b:
                diff = positions_a[i] - positions_b[j]
                # TODO: figure out why did I do "diff > 0?"
                # if diff > 0 and diff <= proximity_upper_bound:
                if abs(diff) <= proximity_upper_bound:
                    res.append(docID)
                    break
                elif diff < 0:
                    i += 1
                else:
                    j += 1

        return res
