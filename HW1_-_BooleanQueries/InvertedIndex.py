import os
import re

class InvertedIndex:

    def __init__(self, path: str):
        self.AP_wordmap = {}
        self.path = str(path)
        self.doc_counter = 0

    def parse_file_string(self, file_path):
        with open(file_path, 'r') as AP_file:
            file_string = AP_file.read()
            doc_list = file_string.split(sep="<DOC>")[1:]
            doc_list = [str(doc).replace("\n", '') for doc in doc_list]
            doc_list = [(re.search('<DOCNO>(.+?)</DOCNO>', doc).group(1).strip(),
                         re.search('<TEXT>(.+?)</TEXT>', doc).group(1).strip()) for doc in doc_list]
        yield from doc_list

    def get_next_doc(self):

        # iterate through all files
        for file in os.listdir():
            file_path = os.path.join(self.path, file)
            yield from self.parse_file_string(file_path)

    def tokenize(self):
        os.chdir(self.path)
        for i in [1, 2, 3, 4]:
            print(self.get_next_doc())
        return self


if __name__ == '__main__':
    path = "data/HW1/AP_Coll_Parsed"
    InvertedIndex(path).tokenize()
