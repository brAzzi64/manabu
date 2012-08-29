# -*- coding: utf-8 -*-

import urllib2
import HTMLParser
import furiganizer

class SentenceParser(HTMLParser.HTMLParser):
    def __init__(self):
        HTMLParser.HTMLParser.__init__(self)
        self.phrases = []

    def feed(self, data):
        self.phrases = []
        HTMLParser.HTMLParser.feed(self, data)

    def handle_starttag(self, tag, attributes):
        if tag == 'a':
            for (attr, value) in attributes:
                if attr == 'href':
                    if value.find('/kanji/details/') == 0:
                        self.phrases.append( value[15:] )
                    break

    def get_sentences(self):
        return self.phrases


class SentenceGrabber:
    def __init__(self, kanji):
        self.page = 1
        self.url = "http://jisho.org/sentences?jap=" + kanji.encode('utf-8') + "&page="
        self.parser = SentenceParser()
        self.furi = furiganizer.Furiganizer()
        self.sentences = []

    def get_next_page(self):
        url = self.url + str(self.page)
        u = urllib2.urlopen(url)
        encoding = u.headers.getparam('charset')

        # parse it
        self.parser.feed( u.read().decode(encoding) )
        new_sentences = self.parser.get_sentences()

        # analyze the sentences
        analyzed = []
        for s in new_sentences:
            self.furi.feed(s)
            analyzed.append( self.furi.get_string() )

        self.sentences += zip(new_sentences, analyzed)
        self.page += 1

    def get_processed_page_count(self):
        return self.page - 1

