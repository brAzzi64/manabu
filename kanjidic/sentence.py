# -*- coding: utf-8 -*-

import urllib2
import HTMLParser
import thread
import time


def get_value(attrs, first):
    for (key,value) in attrs:
        if key == first:
            return value
    return None

# TODO: use pyquery to do this HTML parsing for simpler code
class SentenceParser(HTMLParser.HTMLParser):
    def __init__(self):
        HTMLParser.HTMLParser.__init__(self)
        self.phrases = []
        self.trackings = {}
        self.phrase_japanese = None

    def feed(self, data):
        HTMLParser.HTMLParser.feed(self, data)

    def get_sentences(self):
        ret = self.phrases
        self.phrases = []
        return ret

    # handle parsing events
    def handle_starttag(self, tag, attrs):
        if tag == 'td' and get_value(attrs, 'class') == 'japanese':
            self.track_node('td_japanese')
        if tag == 'td' and get_value(attrs, 'class') == 'english':
            self.track_node('td_english')
        self.track_starttag()

    def handle_endtag(self, tag):
        tup = self.track_endtag()
        if tup != None:
            (name, data) = tup
            if name == 'td_japanese':
                self.phrase_japanese = data
            elif name == 'td_english':
                self.phrases.append((self.phrase_japanese, data))
                self.phrase_japanese = None
        # TODO: some kind of error handling?

    def handle_data(self, data):
        self.track_data(data)

    # node tracking
    def track_node(self, name):
        self.trackings[name] = [0, ""]

    def track_starttag(self):
        for name in self.trackings.keys():
            self.trackings[name][0] += 1

    def track_endtag(self):
        for name in self.trackings.keys():
            self.trackings[name][0] -= 1
            if self.trackings[name][0] == 0:
                data = self.trackings[name][1].strip()
                del self.trackings[name]
                # only one tag should end, so
                # no need to keep iterating
                return (name, data)

    def track_data(self, data):
        for name in self.trackings.keys():
            self.trackings[name][1] += data


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

