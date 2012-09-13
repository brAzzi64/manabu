# -*- coding: utf-8 -*-
import urllib2
import thread
import time
import string
import re

from jishopar import JishoParser
from tatopar import TatoebaParser
from kanjidic import Kanji, KanjiDic
from restructurer import Restructurer


class SentenceGrabber:
    def __init__(self, kanji):
        self.j_url = "http://jisho.org/sentences?jap=" + kanji.encode('utf-8') + "&page="
        self.t_url = "http://tatoeba.org/eng/sentences/search?query=%s&from=jpn&to=und"
        self.j_parser = JishoParser()
        self.t_parser = TatoebaParser()
        self.restructurer = Restructurer()
        self.kc = KanjiDic()
        self.sentences = []
        self.finished = False
        # start grabbing sentences
        thread.start_new_thread(SentenceGrabber.start_getting_sentences, (self,))

    def pop_next_sentence(self):
        total_sleep = 0
        print "Waiting to POP sentence..."
        while len(self.sentences) == 0 and total_sleep < 60:
            time.sleep(0.2)
            total_sleep += 0.2
        print "Popped! (%.3fms)" % (total_sleep)
        return self.sentences.pop(0) if len(self.sentences) > 0 else None

    def start_getting_sentences(self):
        jisho_page = 1
        while jisho_page < 5: # TODO: change the stopping condition
            print "Downloading Jisho page #%d" % jisho_page
            url = self.j_url + str(jisho_page)
            u = urllib2.urlopen(url)
            encoding = u.headers.getparam('charset')
            # parse it
            self.j_parser.feed( u.read().decode(encoding) )
            jisho_sentences = self.j_parser.get_sentences()
            for i, bun in enumerate(jisho_sentences):
                # TODO: filter by known kanjis
                print "Downloading Tatoeba sentence #%d" % (i+1)
                url = self.t_url % bun.encode('utf-8')
                u = urllib2.urlopen(url)
                # parse it
                (structure_orig, translations) = self.t_parser.feed( u.read().decode('utf-8'), bun )
                # adjust the structure to our format
                structure = self.restructurer.feed(structure_orig)
                # get kanji pronunciations
                pronunciations = self.get_pronunciations(bun)
                # add it to the collection
                self.sentences += [ { 'sentence' : bun, 'structure' : structure, 'structure_orig' : structure_orig, 'translations' : translations, 'pronunciations' : pronunciations } ]
            jisho_page += 1
        self.finished = True

    def any_sentence_left(self):
        return len(self.sentences) > 0 or not self.finished

    def get_pronunciations(self, sentence):
        mappings = {}
        kanjis = set(l for l in sentence if Restructurer.is_kanji(l))
        for literal in kanjis:
            onyomis = []
            kunyomis = []
            try:
                kanji = self.kc[literal]
                onyomis = list(kanji.onyomis)
                kunyomis = list(kanji.kunyomis)
            except Exception as e:
                print u"No information for Kanji: %s" % literal
                print e
            mappings[literal] = { 'ON' : onyomis, 'KN' : kunyomis }
        return mappings

if __name__ == '__main__':
    sg = SentenceGrabber('私')
    while True:
        s = sg.pop_next_sentence()
        if s == None:
            break
        print u"%s, %s, %s" % (s['sentence'], s['structure'], s['translation'])

