# -*- coding: utf-8 -*-

import sys; sys.path.append('../kanjidic')
from import_kolivas import get_kolivas_mapping
from sentence import SentenceGrabber

# this implements the proof of concept:
# it is indeed viable to find sentences with the new kanji when at least 100 kanjis are known

def is_kanji(c):
    return ord(c) > 0x4E00 and ord(c) < 0x9FFF

def all_known_kanjis(sentence, known_kanjis):
    kanjis = [k for k in sentence if is_kanji(k)]
    unknown = [k for k in kanjis if k not in known_kanjis]
    return unknown == []


mapping = get_kolivas_mapping()
first_kanjis = [k for k in mapping if mapping[k] <= 10]
first_kanjis = sorted(first_kanjis, key = lambda x: mapping[x])

for k in first_kanjis:
    print "%s:" % k
    sentences = []
    sg = SentenceGrabber(k)
    bun = sg.pop_next_sentence()
    while bun != None and len(sentences) < 3:
        if all_known_kanjis(bun, first_kanjis) and bun not in sentences:
            sentences.append(bun)
        bun = sg.pop_next_sentence()
    for s in sentences:
        print u"　　" + s

