# -*- coding: utf-8 -*-
import urllib2
import thread
import time
import string
import re

from optparse import OptionParser

from bun.jishopar import JishoParser
from bun.tatopar import TatoebaParser
from bun.restructurer import Restructurer
from bun.kanjidic import KanjiDic, Kanji


class SentenceGrabber:
    def __init__(self, kanji, page_range):
        self.j_url = "http://jisho.org/sentences?jap=" + kanji.encode('utf-8') + "&page="
        self.t_url = "http://tatoeba.org/eng/sentences/search?query=%s&from=jpn&to=und"
        self.j_parser = JishoParser()
        self.t_parser = TatoebaParser()
        self.restructurer = Restructurer()
        self.sentences = []
        self.finished = False
        self.first_page = page_range[0]
        self.last_page = page_range[1]
        # start grabbing sentences
        # TODO: handle the thread termination when when object is destroyed
        thread.start_new_thread(SentenceGrabber.start_getting_sentences, (self,))
        print u"Starting grab for kanji: %s" % kanji

    def pop_next_sentence(self):
        total_sleep = 0
        print "Waiting to POP sentence..."
        while len(self.sentences) == 0 and total_sleep < 60:
            time.sleep(0.2)
            total_sleep += 0.2
        print "Popped! (%.3fms)" % (total_sleep)
        return self.sentences.pop(0) if len(self.sentences) > 0 else None

    def start_getting_sentences(self):
        jisho_page = self.first_page
        while jisho_page <= self.last_page:
            print "Downloading Jisho page #%d" % jisho_page
            url = self.j_url + str(jisho_page)
            u = urllib2.urlopen(url)
            encoding = u.headers.getparam('charset')
            # parse it
            self.j_parser.feed( u.read().decode(encoding) )
            jisho_sentences = self.j_parser.get_sentences()
            for i, bun in enumerate(jisho_sentences):
                print "Downloading Tatoeba sentence #%d" % (i+1)
                url = self.t_url % bun.encode('utf-8')
                u = urllib2.urlopen(url)
                # parse it
                (structure_orig, translations) = self.t_parser.feed( u.read().decode('utf-8'), bun )
                # adjust the structure to our format
                structure = self.restructurer.feed(structure_orig)
                # add it to the collection
                self.sentences += [ { 'sentence' : bun, 'structure' : structure, 'structure_orig' : structure_orig, 'translations' : translations } ]
            jisho_page += 1
        self.finished = True

    def any_sentence_left(self):
        return len(self.sentences) > 0 or not self.finished

# run from /other folder with:
# PYTHONPATH=`pwd`/.. python import_sentences.py --kanji-range=1:2 --page-range=1:3
if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-k", "--kanji-range", dest = "kanjirange")
    parser.add_option("-p", "--page-range", dest = "pagerange")
    (options, args) = parser.parse_args()

    # parse Kanji Range
    krange = (1,100)
    if options.kanjirange != None:
        rng = options.kanjirange.split(":")
        krange = ( int(rng[0]), int(rng[1]) )

    # parse Page Range
    prange = (1,5)
    if options.pagerange != None:
        rng = options.pagerange.split(":")
        prange = ( int(rng[0]), int(rng[1]))

    kd = KanjiDic('.')
    m = kd.get_kolivas_mapping()
    inv_kolivas_map = dict((m[k], k) for k in m.keys())

    # for each kanji in the range
    for k in range(*krange):
        kanji = inv_kolivas_map[k]
        sg = SentenceGrabber(kanji, prange)
        while True:
            s = sg.pop_next_sentence()
            if s == None:
                break
            #print u"%s, %s, %s" % (s['sentence'], s['structure'], s['translations'])
            print u"%s, %s, %s" % (s['sentence'], s['structure'], string.join( s['translations'], u"|" ) )

