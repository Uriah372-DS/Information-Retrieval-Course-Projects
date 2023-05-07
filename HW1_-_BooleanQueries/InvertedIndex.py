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
        self.posting_lists = {}
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
            with open(os.path.join(self.path, file_path), 'r') as AP_file:
                file_string = AP_file.read().replace("\n", '')
                for doc in re.finditer(r'<DOC>\s*(.+?)\s*</DOC>', file_string):
                    doc_data = doc.group(1)
                    doc_number = re.search(r'<DOCNO>\s*(.+?)\s*</DOCNO>', doc_data)[1]
                    internal_id += 1
                    for doc_text in re.finditer(r'<TEXT>\s*(.+?)\s*</TEXT>', doc_data):
                        doc_text_data = doc_text.group(1)
                        self.docs_to_ids[doc_number] = internal_id
                        self.ids_to_docs[internal_id] = doc_number
                        self.update_posting_lists(doc_text=doc_text_data, internal_id=internal_id)
                        del doc_text
                        del doc_text_data
        return self

    def update_posting_lists(self, doc_text: str, internal_id):
        # remove duplicates from text and iterate over words:
        for word in [*set(doc_text.split())]:
            if word not in self.posting_lists.keys():
                self.posting_lists[word] = []
            # TODO: optimize this check, using the fact that the lists are sorted, so search from end to start:
            if not self.is_id_in_posting_list(internal_id, self.posting_lists[word]):
                self.posting_lists[word].append(internal_id)

    def is_id_in_posting_list(self, id_number: int, posting_list: list[int]):
        for i in range(start=len(posting_list) - 1, stop=-1, step=-1):
            if posting_list[i] < id_number:
                return False

        return id_number in posting_list

    def get_posting_list(self, term):
        """
        Return the posting list for the given term from the index.
        If the term is not in the index, return an empty list.
        :param term: a word
        :return: list of document ids in which the term appears
        """
        return [] if term not in self.posting_lists.keys() else self.posting_lists[term]


if __name__ == '__main__':
    path = "data/HW1/AP_Coll_Parsed"
    index = InvertedIndex(path)
    # for k, v in index.posting_lists.items():
    #     print(k + ': ' + str(v))

    # part 3:
    print("The top 10 terms with the highest document frequency:")
    for i, term in enumerate(sorted(index.posting_lists.keys(),
                                    key=lambda x: len(index.posting_lists[x]),
                                    reverse=True)[:10]):
        print(str(i + 1) + ": " + term)
    print()

    print("The top 10 terms with the lowest document frequency:")
    for i, term in enumerate(sorted(index.posting_lists.keys(),
                                    key=lambda x: len(index.posting_lists[x]),
                                    reverse=False)[:10]):
        print(str(i + 1) + ": " + term)
    print()

    print("The different characteristics of the above two sets of terms:")
    print("The terms with the highest df are the terms that appear in the highest amount of documents in the corpus.")
    print("The terms with the highest df are the terms that appear in the lowest amount of documents in the corpus.")

#The top 10 terms with the highest document frequency:
# 1: the
# 2: of
# 3: in
# 4: a
# 5: and
# 6: to
# 7: for
# 8: said
# 9: on
# 10: that
#
# The top 10 terms with the lowest document frequency:
# 1: australiavietnam
# 2: radelats
# 3: detered
# 4: nspca
# 5: metveit
# 6: wettre
# 7: toralf
# 8: 283031
# 9: weekwas
# 10: mothibe
