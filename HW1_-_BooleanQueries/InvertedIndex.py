import os
import re


class InvertedIndex:
    def __init__(self, collection_path: str):
        """
        Initialize the inverted index from the AP collection.

        During index construction, specifically, for building the posting lists you should use successive integers as
        document internal identifiers (IDs) for optimizing query processing, as taught in class, but you still need to
        be able to get the original document ID when required.

        :param collection_path: path to the AP collection
        """
        self.wordmap = {}
        # format example:
        # {'the': [1, 2],
        # 'sanctions': [2, 4],
        # 'african': [3, ]}
        self.docs_to_ids = {}  # one-to-one mapping from doc numbers to ids.
        self.ids_to_docs = {}  # one-to-one mapping from doc numbers to ids.
        self.path = str(collection_path)
        self.doc_counter = 0
        self.tokenize()

    def tokenize(self):
        """
        Build the map from words to document ids, and give the documents their internal ids.
        :return:
        """
        # iterate through all files
        internal_id = 0
        for file_path in os.listdir(self.path):
            doc_list = self.parse_file_string(os.path.join(self.path, file_path))
            for doc in doc_list:
                internal_id += 1
                self.docs_to_ids[doc[0]] = internal_id
                self.ids_to_docs[internal_id] = doc[0]
                self.update_wordmap(doc_text=doc[1], internal_id=internal_id)
        return self

    def get_posting_list(self, term):
        """
        Return the posting list for the given term from the index.
        If the term is not in the index, return an empty list.
        :param term: a word
        :return: list of document ids in which the term appears
        """
        return [] if term not in self.wordmap.keys() else self.wordmap[term]

    def update_wordmap(self, doc_text: str, internal_id):
        # remove duplicates from text:
        doc_words = [*set(doc_text.split())]

        for word in doc_words:
            if word not in self.wordmap.keys():
                self.wordmap[word] = []
            if internal_id not in self.wordmap[word]:
                self.wordmap[word].append(internal_id)

    def parse_file_string(self, file_path):
        with open(file_path, 'r') as AP_file:
            file_string = AP_file.read()
            doc_list = file_string.split(sep="<DOC>")[1:]
            doc_list = [str(doc).replace("\n", '') for doc in doc_list]
            doc_list = [(re.search('<DOCNO>(.+?)</DOCNO>', doc).group(1).strip(),
                         re.search('<TEXT>(.+?)</TEXT>', doc).group(1).strip()) for doc in doc_list]
        return doc_list


if __name__ == '__main__':
    path = "data/HW1/AP_Coll_Parsed"
    index = InvertedIndex(path)
    # for k, v in index.wordmap.items():
    #     print(k + ': ' + str(v))

    # part 3:
    print("The top 10 terms with the highest document frequency:")
    for i, term in enumerate(sorted(index.wordmap.keys(), key=lambda x: len(index.wordmap[x]), reverse=True)[:10]):
        print(str(i + 1) + ": " + term)
    print()

    print("The top 10 terms with the lowest document frequency:")
    for i, term in enumerate(sorted(index.wordmap.keys(), key=lambda x: len(index.wordmap[x]), reverse=False)[:10]):
        print(str(i + 1) + ": " + term)
    print()

    print("The different characteristics of the above two sets of terms:")
    print("The terms with the highest df are the terms that appear in the highest amount of documents in the corpus.")
    print("The terms with the highest df are the terms that appear in the lowest amount of documents in the corpus.")
