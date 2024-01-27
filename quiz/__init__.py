import random
from os import path
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
        self.init_text()
        self.quotes = {}
        self.keyword = {}
        self.keys = {}
        self.keyword2 = {}
        self.active_key_word = ''
        self.init_text('')

    def init(self):
        self.quotes = {}
        self.keyword = {}
        self.keys = {}
        self.keyword2 = {}
        self.active_key_word = ''

    def init_text(self, book_name=''):
        if book_name != '':
            self.book_name = book_name
        self.init()
        file_name = path.join(self.txt_folder, f"{self.book_name}-{self.book_version}.txt")
        print(f"{file_name=}")
        with open(file_name, 'rt',  encoding='utf-8-sig') as fn:
            self.full_text = fn.read()
            lines = [x for x in self.full_text.splitlines() if x > '']
        for line in lines:
            # print(f"{line}")

            r = re.findall(fr'(?:{self.book_name})\s+(\d*:\d*)', line)
            # print(f"{r=}")
            if r is None:
                print(f"No verse info found: {line}")
                continue
            verse = r[0]
            self.quotes[verse] = line

            line = line[line.find(verse):]

            for w in line.split()[1:]:
                w = w.strip(string.punctuation)
                if w in self.ignore_words:
                    continue
                if w in self.keyword:
                    self.keyword[w].append(verse)
                else:
                    self.keyword[w] = [verse]
        self.keys = [x for x in self.keyword.keys() if len(self.keyword[x]) == 1]

    def rand_keyword(self):
        self.active_key_word = random.choice(self.keys)
        return self.active_key_word

    def rand_keyword2(self):
        pass

    def quote_for_key(self, words='', ):
        if words == '':
            words = self.active_key_word
        if words == '':
            return None
        verse = self.keyword[words][0]
        quote = self.quotes[verse]
        # print(f"{'-'*10}In quiz.quote_for_key {'-'*20}\n {words=}, {verse=}, {quote=}")
        return quote


quiz = Quiz()

with open('quiz.dump', 'wb') as fn:
    pickle.dump(quiz, fn)
