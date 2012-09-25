# -*- coding: utf-8 -*-
from restructurer import Restructurer
from common import Singleton


class ISentenceProvider(object):

    def get_sentences(self, kanji, items_per_page, page_num):
        """
        Returns 'items_per_page' sentences from page 'page_num'
        containing 'kanji'. The format of each is a tuple:
            (id, sentence, structure, translations)
        """
        raise NotImplementedError()



import gzip

class FileSentenceProvider(ISentenceProvider):
    __metaclass__ = Singleton

    def __init__(self, datadir = 'other'):
        """ Loads the file with the sentences """
        self.sentences = {}
        datadir = datadir[:-1] if datadir[-1] == "/" else datadir
        with gzip.open(datadir + '/top_1000_kanji_sentences.txt.gz', 'r') as f:
            for id, line in enumerate(f):
                parts = line.decode('utf-8').split(';')
                parts[2] = parts[2].split('|') # split translations into a list
                self.sentences[id] = tuple(parts)
        self.cache = {}

    def get_sentences(self, kanji, items_per_page, page_num):
        """
        Implementation of get_sentences.

        """
        if len(kanji) != 1 or type(kanji) != unicode or not Restructurer.is_kanji(kanji):
            raise ValueError("Invalid value for 'kanji' parameter")

        try:
            query_ids = self.cache[kanji]
        except KeyError:
            query = [ (k, len(v[0])) for (k, v) in self.sentences.items() if kanji in v[1] ]
            query.sort(key = lambda x: x[1])     # sort by second argument, length of the sentence
            query_ids = [ t[0] for t in query ]  # keep only the ids
            self.cache[kanji] = query_ids

        results = [ self.sentences[id] for id in query_ids ]
        init_idx = page_num * items_per_page
        return results[init_idx : init_idx + items_per_page]


if __name__ == '__main__':
    sp = FileSentenceProvider('../other')
    ss = sp.get_sentences(u'語', 30, 0)
    for r in ss:
        print u'%s | %s | %s' % r

