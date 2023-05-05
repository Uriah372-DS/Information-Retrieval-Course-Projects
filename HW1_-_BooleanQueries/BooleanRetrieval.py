from InvertedIndex import InvertedIndex


class BooleanRetrieval:
    def __init__(self, inverted_index: InvertedIndex):
        self.inverted_index = inverted_index
        self.last_results = None

    def retrieve(self, query):
        # splitting query at whitespaces
        query = query.split()

        # stack
        stack = []

        # iterating expression
        for word in query:

            # word is a number
            if word not in ['AND', 'OR', 'NOT']:
                stack.append([s for s in self.inverted_index.wordmap[word]])  # add the LIST of the word instead of the word itself

            # word is an operator
            else:
                # getting operands
                right = stack.pop()
                left = stack.pop()

                # performing operation according to operator
                if word == 'AND':
                    stack.append(self.and_update(left, right))

                elif word == 'OR-':
                    stack.append(self.or_update(left, right))

                elif word == 'NOT':
                    stack.append(self.not_update(left, right))

    def and_update(self, left: list, right):
        pass

    def or_update(self, left, right):
        pass

    def not_update(self, left, right):
        pass


if __name__ == '__main__':
    path = "data/HW1/AP_Coll_Parsed"
    index = InvertedIndex(path)
    index.tokenize()
    boolean_retrieval = BooleanRetrieval(index)
    queries_path = 'data\HW1\BooleanQueries.txt'
    with open(queries_path, 'r') as queries:
        for query in queries.readline():
            boolean_retrieval.retrieve(query)
            print(' '.join(boolean_retrieval.last_results))
