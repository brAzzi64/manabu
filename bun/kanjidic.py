# -*- coding: utf-8 -*-

import sys
import string

from lxml import etree


class Kanji(object):

    def __init__(self, literal, unicode_index, kolivas_index, onyomis, kunyomis):
        """
        Constructs a Kanji element with its indexes and pronunciations.

        """
        self.literal = literal
        self.idx_unicode = unicode_index
        self.idx_kolivas = kolivas_index
        self.onyomis = onyomis
        self.kunyomis = kunyomis

    def __unicode__(self):
        return u"<Kanji: %s (u:%d,k:%d)>" % (self.literal, self.idx_unicode, self.idx_kolivas)


class KanjiDic(object):

    def __init__(self):
        """
        Constructs the Kanji Dictionary from the XML file.

        """
        self.kanjis = {}

        print "Reading KANJIDIC...",

        tree = etree.parse('other/kanjidic2.xml.gz')
        query = u"/kanjidic2/character[misc/freq]" # characters with freq node
        nodes = tree.xpath(query)
        total_nodes = len(nodes)

        # get the kolivas indexes
        kolivas_mapping = self.get_kolivas_mapping(total_nodes)

        for cnode in nodes:
            char = cnode.xpath(u"literal")[0].text
            onyomis = []
            kunyomis = []
            pnodes = cnode.xpath(u"reading_meaning/rmgroup/reading[@r_type='ja_on' or @r_type='ja_kun']")

            for pnode in pnodes:
                if pnode.attrib['r_type'] == u'ja_on':
                    onyomis.append( pnode.text )
                elif pnode.attrib['r_type'] == u'ja_kun':
                    kunyomis.append( pnode.text )

            # add the kanji to the dictionary
            self.kanjis[char] = Kanji(char, ord(char), kolivas_mapping.get(char), onyomis, kunyomis)

        print "Done (%d read)." % total_nodes

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

    def get_kolivas_mapping(self, max_kanjis):
        """
        Returns the mapping of each Kanji to its Kolivas index.

        """
        mapping = {}

        tree = etree.parse('other/kanji.html.gz')
        nodes = tree.xpath("//span[@class='c1' and text()]")[:max_kanjis]

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

