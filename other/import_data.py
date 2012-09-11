# -*- coding: utf-8 -*-

# setup the environment
from django.core.management import setup_environ
import settings

setup_environ(settings)

# real script
import sys
import string
import import_kolivas

from lxml import etree
from bun.models import Kanji, Pronunciation
from django.db import transaction

tree = etree.parse( open('kanjidic2.xml', 'r') )
query = u"/kanjidic2/character[misc/freq]" # characters with freq node
nodes = tree.xpath(query)

total_nodes = len(nodes)
added_nodes = 0

# get the kolivas indexes
kolivas_mapping = import_kolivas.get_kolivas_mapping()

def get_kolivas(k):
    try:
        return kolivas_mapping[k]
    except KeyError:
        return None

with transaction.commit_on_success():
    for cnode in nodes:
        char = cnode.xpath(u"literal")[0].text
        k = Kanji(character = char, unicode_index = ord(char), kolivas_index = get_kolivas(char))
        k.save()

        pnodes = cnode.xpath(u"reading_meaning/rmgroup/reading[@r_type='ja_on' or @r_type='ja_kun']")
        for pnode in pnodes:
            reading = u'ON' if pnode.attrib['r_type'] == u'ja_on' else u'KN'
            p = Pronunciation.objects.filter(text = pnode.text)
            if len(p) == 0:
                p = Pronunciation(ptype = reading, text = pnode.text)
                p.save()
            else:
                p = p[0] # there should be only one
            k.pronunciations.add(p)
        k.save()

        added_nodes += 1
        print "Imported kanji %d/%d" % (added_nodes, total_nodes)

