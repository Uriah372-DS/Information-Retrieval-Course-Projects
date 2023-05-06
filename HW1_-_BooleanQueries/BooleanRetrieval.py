from InvertedIndex import InvertedIndex


class BooleanRetrieval:
    def __init__(self, inverted_index: InvertedIndex):
        """
        Initialize the boolean retrieval model.
        """
        self.inverted_index = inverted_index
        self.last_results = None

    def run_query(self, query):
        """
        Run the given query on the index.
        :param query: a boolean query
        :return: list of document ids
        """
        # splitting query at whitespaces
        query = query.split()

        # stack
        stack = []

        # iterating expression
        for word in query:

            # word is a term
            if word not in ['AND', 'OR', 'NOT']:
                if word in self.inverted_index.wordmap:
                    stack.append([s for s in self.inverted_index.wordmap[word]])  # add the LIST of the word instead of the word itself
                else:
                    stack.append([])

            # word is an operator
            else:
                # getting operands
                right = stack.pop()
                left = stack.pop()

                # performing operation according to operator
                if word == 'AND':
                    stack.append(self.and_update(left, right))
                elif word == 'OR':
                    stack.append(self.or_update(left, right))
                elif word == 'NOT':
                    stack.append(self.not_update(left, right))

        self.last_results = stack.pop()
        self.last_results = [self.inverted_index.ids_to_docs[id] for id in self.last_results]
        return self.last_results

    def and_update(self, left: list, right: list):
        temp = []
        li = ri = 0
        m = len(left)
        n = len(right)
        while li < m and ri < n:
            if left[li] == right[ri] and right[ri] not in temp:
                temp.append(right[ri])
            elif left[li] < right[ri]:
                li += 1
            else:
                ri += 1
        return temp

    def or_update(self, left, right):
        # finds value in left that are not in right, and inserts them in place
        ri = 0
        n = len(right)
        for val in left:
            while ri < n and right[ri] < val:
                ri += 1
            if ri < n and right[ri] != val:
                right.insert(ri, val)
                ri += 1
            if ri >= n:
                right.append(val)
        return right

    def not_update(self, left, right):
        index_l = 0
        m = len(left)
        for val in right:
            while index_l < m and left[index_l] < val:
                index_l += 1
            if index_l < m and val == left[index_l]:
                left.pop(index_l)
        return left


if __name__ == '__main__':
    path = "data/HW1/AP_Coll_Parsed"
    index = InvertedIndex(path)
    index.tokenize()
    boolean_retrieval = BooleanRetrieval(index)
    queries_path = 'data\HW1\BooleanQueries.txt'
    results = []
    with open(queries_path, 'r') as queries:
        for query in queries.readlines():
            boolean_retrieval.run_query(query)
            results.append(' '.join(boolean_retrieval.last_results))

    for i in range(5):
        with open("Part_2.txt", 'a') as output:
            print(results[i])
            output.write(results[i] + '\n')
