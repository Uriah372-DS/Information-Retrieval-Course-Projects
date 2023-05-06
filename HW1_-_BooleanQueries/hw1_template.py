# Part 1: InvertedIndex
class InvertedIndex:
    def __init__(self, collection_path):
        """
        Initialize the inverted index from the AP collection.

        During index construction, specifically, for building the posting lists you should use successive integers as
        document internal identifiers (IDs) for optimizing query processing, as taught in class, but you still need to
        be able to get the original document ID when required.

        :param collection_path: path to the AP collection
        """
        pass

    def get_posting_list(self, term):
        """
        Return the posting list for the given term from the index.
        If the term is not in the index, return an empty list.
        :param term: a word
        :return: list of document ids in which the term appears
        """
        pass


# Part 2: Boolean Retrieval Model
class BooleanRetrieval:
    def __init__(self, inverted_index):
        """
        Initialize the boolean retrieval model.
        """
        pass

    def run_query(self, query):
        """
        Run the given query on the index.
        :param query: a boolean query
        :return: list of document ids
        """
        return []


if __name__ == "__main__":

    # TODO: replace with the path to the AP collection and queries file on your machine
    path_to_AP_collection = '<path_to_AP_collection>'
    path_to_boolean_queries = '<path_to_boolean_queries>'

    # Part 1
    inverted_index = InvertedIndex(path_to_AP_collection)

    # Part 2
    boolean_retrieval = BooleanRetrieval(inverted_index=inverted_index)

    # Read queries from file
    with open(path_to_boolean_queries, 'r') as f:
        queries = f.readlines()

    # Run queries and write results to file
    with open("Part_2.txt", 'w') as f:
        for query in queries:
            result = boolean_retrieval.run_query(query)
            f.write(' '.join(result) + '\n')

    # Part 3
    # TODO: write here your code for part 3
