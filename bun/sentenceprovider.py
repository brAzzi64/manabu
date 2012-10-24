# -*- coding: utf-8 -*-
from restructurer import Restructurer
from common import Singleton


class ISentenceProvider(object):

    def get_sentences(self, kanji, items_per_page, page_num, allowed_kanji):
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

    def get_sentences(self, kanji, items_per_page, page_num, allowed_kanji = None):
        """
        Implementation of get_sentences.

        """
        if len(kanji) != 1 or type(kanji) != unicode or not Restructurer.is_kanji(kanji):
            raise ValueError("Invalid value for 'kanji' parameter")

        # add the kanji to search to the list of allowed kanji
        if not allowed_kanji is None:
            allowed_kanji += kanji

        try:
            query_ids = self.cache[kanji]
        except KeyError:
            query = [ (k, len(v[0])) for (k, v) in self.sentences.items() \
                      if kanji in v[0] \
                         and v[1] != '' \
                         and ( allowed_kanji is None \
                               or self.all_allowed(v[0], allowed_kanji) ) ]
            # with v[1] != '' we filter bad data (TODO: sanitize bad data)
            query.sort(key = lambda x: x[1])     # sort by second argument, length of the sentence
            query_ids = [ t[0] for t in query ]  # keep only the ids
            self.cache[kanji] = query_ids

        results = [ self.sentences[id] for id in query_ids ]
        init_idx = page_num * items_per_page
        return results[init_idx : init_idx + items_per_page]

    def all_allowed(self, sentence, allowed):
        return all((c in allowed for c in sentence if Restructurer.is_kanji(c)))


if __name__ == '__main__':
    sp = FileSentenceProvider('../other')
    ss = sp.get_sentences(u'語', 30, 0)
    for r in ss:
        print u'%s | %s | %s' % r

