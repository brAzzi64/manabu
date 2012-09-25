# -*- coding: utf-8 -*-

import sys
import string

from lxml import etree
from common import Singleton


class Kanji(object):

    def __init__(self, literal, unicode_index, kolivas_index, onyomis, kunyomis):
        """
        Constructs a Kanji element with its indexes and pronunciations.

        """
        self.literal = literal
        self.idx_unicode = unicode_index
        self.idx_kolivas = kolivas_index
        self.idx_unisort = -1
        self.onyomis = onyomis
        self.kunyomis = kunyomis

    def __unicode__(self):
        return u"<Kanji: %s (u:%d,k:%d)>" % (self.literal, self.idx_unicode, self.idx_kolivas)


class KanjiDic(object):
    __metaclass__ = Singleton

    def __init__(self, datadir = 'other'):
        """
        Constructs the Kanji Dictionary from the XML file.

        """
        self.kanjis = {}
        self.datadir = datadir[:-1] if datadir[-1] == "/" else datadir

        print "Loading KANJIDIC...",
        sys.stdout.flush()

        tree = etree.parse(self.datadir + '/kanjidic2.xml.gz')
        query = u"/kanjidic2/character"
        nodes = tree.xpath(query)

        # get the kolivas indexes
        kolivas_mapping = self.get_kolivas_mapping()

        for cnode in nodes:
            char = cnode.xpath(u"literal")[0].text
            onyomis = []
            kunyomis = []
            pnodes = cnode.xpath(u"reading_meaning/rmgroup/reading[@r_type='ja_on' or @r_type='ja_kun']")
            kolivas_idx = kolivas_mapping.get(char)

            # add only Jouyou Kanji, the
            # ones present in Kolivas indexing
            if kolivas_idx != None:
                for pnode in pnodes:
                    if pnode.attrib['r_type'] == u'ja_on':
                        onyomis.append( pnode.text )
                    elif pnode.attrib['r_type'] == u'ja_kun':
                        kunyomis.append( pnode.text )

                # add the kanji to the dictionary
                self.kanjis[char] = Kanji(char, ord(char), kolivas_mapping.get(char), onyomis, kunyomis)

        # set the unisort indexes (index in an the array of Jouyou sorted by idx_unicode)
        sorted_kanji = sorted(self.kanjis.keys(), key = lambda x: self.kanjis[x].idx_unicode)
        for i, sk in enumerate(sorted_kanji):
            self.kanjis[sk].idx_unisort = i

        print "Done (%d loaded)." % len(self.kanjis)

    def __getitem__(self, literal):
        """
        Returns the Kanji object for the specified literal.

        """
        if not isinstance(literal, unicode) or len(literal) != 1:
            raise TypeError

        return self.kanjis[literal]

    def keys(self):
        """
        Returns the set of keys.

        """
        return self.kanjis.keys()

    def get_kolivas_mapping(self):
        """
        Returns the mapping of each Kanji to its Kolivas index.

        """
        mapping = {}

        tree = etree.parse(self.datadir + '/kanji.html.gz')
        nodes = tree.xpath("//span[@class='c1' and text()]")

        for (i, node) in enumerate(nodes):
            mapping[node.text.strip()] = i + 1

        return mapping



if __name__ == '__main__':

    kd = KanjiDic()

    # test 1
    kanji = kd[u'私']
    print(u"%s" % kanji)

    # test 2
    try:
        kanji = kd["h"]
    except TypeError:
        print("TypeError thrown: invalid key type (not unicode)")

    # test 3
    try:
        kanji = kd[u"私僕"]
    except TypeError:
        print("TypeError thrown: invalid key type (not 1 character long)")

    # test 4
    try:
        kanji = kd[u"か"]
    except KeyError:
        print("KeyError thrown: key not present")

    #def my_print(m): print m,
    #map(my_print, kd.keys())

