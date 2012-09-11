import string
from pyquery import PyQuery

class JishoParser():
    def __init__(self):
        self.phrases = []

    def feed(self, data):
        d = PyQuery(data)
        for node in d("table > tr:not(.lower) .japanese"):
            tr = PyQuery(node)
            sentence = string.join( tr.text().split(' '), "" ).strip()
            self.phrases.append(sentence)

    def get_sentences(self):
        ret = sorted(self.phrases, key = len)
        self.phrases = []
        return ret

