from pyquery import PyQuery

class TatoebaParser():
    def __init__(self):
        self.tuple = []

    def feed(self, data, sentence):
        d = PyQuery(data)
        sets = d(".sentences_set")
        for s in sets:
            s = PyQuery(s)
            if s.find(".mainSentence .sentenceContent a").text().strip() == sentence:
                structure = s.find(".mainSentence .sentenceContent .romanization.furigana").text()
                translations = s.find(".translations:first") \
                                .find(".sentence > img[title='English']") \
                                .parent().find(".sentenceContent > a") \
                                .map(lambda i, o: o.text)
                return (structure, translations)
        return (None, None)

