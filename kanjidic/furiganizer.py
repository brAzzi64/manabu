# -*- coding: utf-8 -*-

import sys
import MeCab

class Furiganizer:
    def __init__(self):
        self.tagger = MeCab.Tagger()
        self.data = []

    def feed(self, sentence):
        self.sentence = sentence
        self.data = []
        node = self.tagger.parseToNode( self.sentence.encode('utf-8') )
        node = node.next
        while node and node.surface != '':
            self.data.append( (unicode(node.surface, 'utf-8'), unicode(node.feature, 'utf-8')) )
            node = node.next

    def get_string(self):
        string = ""
        for (s,f) in self.data:
            string += s
            if self.has_kanji(s):
                string += '[' + f.split(',')[5] + ']'
            string += ' '
        return string

    @staticmethod
    def has_kanji(sentence):
        for c in sentence:
            if ord(c) > 0x4E00 and ord(c) < 0x9FFF:
                return True
        return False


if __name__ == '__main__':
    f = Furiganizer()
    f.feed( unicode(sys.argv[1], 'utf-8') )
    #f.feed('私は偶然彼に出会った。')
    print f.get_string()

