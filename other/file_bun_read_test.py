#!/usr/bin/python
# run from 'other/' directory
import gzip

def get_sentences():
    sentences = []
    with gzip.open('top_1000_kanji_sentences.txt.gz', 'r') as g:
        for line in g:
            sentences.append( tuple( line.decode('utf-8').split(';') ) )
    return sentences


