# -*- coding: utf-8 -*-

import urllib2
import HTMLParser
import thread
import time


class SentenceParser(HTMLParser.HTMLParser):
    def __init__(self):
        HTMLParser.HTMLParser.__init__(self)
        self.phrases = []

    def feed(self, data):
        HTMLParser.HTMLParser.feed(self, data)

    def handle_starttag(self, tag, attributes):
        if tag == 'a':
            for (attr, value) in attributes:
                if attr == 'href':
                    if value.find('/kanji/details/') == 0:
                        self.phrases.append( value[15:] )
                    break

    def get_sentences(self):
        ret = self.phrases
        self.phrases = []
        return ret


class SentenceGrabber:
    def __init__(self, kanji):
        self.url = "http://jisho.org/sentences?jap=" + kanji.encode('utf-8') + "&page="
        self.parser = SentenceParser()
        self.sentences = []
        thread.start_new_thread(SentenceGrabber.start_getting_sentences, (self,))

    def pop_next_sentence(self,):
        total_sleep = 0
        while len(self.sentences) == 0 and total_sleep < 5:
            time.sleep(0.2)
            total_sleep += 0.2
        return self.sentences.pop(0) if len(self.sentences) > 0 else None

    def start_getting_sentences(self):
        page = 1
        while page < 5: # TODO: change the stopping condition
            url = self.url + str(page)
            u = urllib2.urlopen(url)
            encoding = u.headers.getparam('charset')
            # parse it
            self.parser.feed( u.read().decode(encoding) )
            self.sentences += self.parser.get_sentences()
            page += 1

    def remaining_sentences_count(self):
        return len(self.sentences)

