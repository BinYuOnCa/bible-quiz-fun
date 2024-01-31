import random
from os import path, listdir
import re
import string
import pickle


class Quiz:
    def __init__(self, book_name='Philippians'):
        self.full_text = ''
        self.book_name = book_name
        self.book_version = 'NIV'
        self.txt_folder = 'bible_txt'
        self.ignore_words = {'I', 'of', 'in', 'at'}
        self.quotes = {}
        self.keyword = {}
        self.keys = []
        self.keyword2 = {}
        self.active_key_word = ''
        self.active_verse = ''
        self.init_books()

    def init(self, book_name='Philippians'):
        self.quotes = {}
        self.keyword = {}
        self.keys = []
        self.keyword2 = {}
        self.active_key_word = ''
        self.active_verse = ''
        self.book_name = book_name
        self.init_books()

    def init_books(self):
        for file in listdir(self.txt_folder):
            book_name = re.findall(r"[a-zA-Z1-9]+", file)[0]
            version = re.findall(r"(?:-)([A-Z]+)", file)[0]
            ext_name = re.findall(r"[a-z]+$", file)[0]

            # print(f"init books: {file=}, {book_name=}, {version=}, {ext_name=}")
            if ext_name != 'txt':
                continue
            lines = self.read_book(book_name, version)
            if lines is None:
                continue
            self.process_book(book_name, lines)

        self.keys = [x for x in self.keyword.keys() if len(self.keyword[x]) == 1]

    def read_book(self, book_name, version):
        # print(f"start read_book({book_name=}, {version=})")
        if book_name is None:
            return
        full_name = path.join(self.txt_folder, f"{book_name}-{version}.txt")
        print(f"{full_name=}")

        if not path.isfile(full_name):
            return
        with open(full_name, 'rt',  encoding='utf-8-sig') as fn:
            return [x for x in fn.read().splitlines() if x > '']

    def process_book(self, book_name, lines):
        for line in lines:
            r = re.findall(fr"(?:{book_name})\s+(\d+:\d+)", line)
            if r is None:
                continue
            verse = r[0]
            self.quotes[(book_name,verse)] = line

            txt = line[line.find(verse):]
            for w in txt.split()[1:]:
                w = w.strip(string.punctuation)
                if w in self.ignore_words:
                    continue
                if w in self.keyword:
                    self.keyword[w].append((book_name, verse))
                else:
                    self.keyword[w] = [(book_name, verse)]

    def rand_keyword(self):
        while True:
            key = random.choice(self.keys)
            book_name, verse = self.keyword[key][0]
            # print(f"rand_keyword: {key=} in {book_name=}, {verse=}, {self.book_name=}")
            if book_name == self.book_name:
                break

        self.active_key_word = key
        self.active_verse = verse
        return key

    def rand_keyword2(self):
        pass

    def quote_for_key(self, words='', ):
        if words == '':
            words = self.active_key_word
        if words == '':
            return None

        book_name, verse = self.keyword[words][0]
        quote = self.quotes[(book_name, verse)]
        # print(f"Quote by words: {words=},{book_name=},{verse=} \n {quote=}")
        # quote = self.quotes[(self.book_name, self.active_verse)]
        # print(f"{'-'*10}In quiz.quote_for_key {'-'*20}\n "
        #       f"{words=},{self.book_name=}, {self.active_verse=}\n"
        #       f" {quote=}")
        return re.sub(fr'( {verse}|[^a-zA-Z0-9]{words}[^a-zA-Z0-9]*)',
                      r'<b style="color:red;">\1</b>', quote)


quiz = Quiz()

with open('quiz.dump', 'wb') as fn:
    pickle.dump(quiz, fn)
