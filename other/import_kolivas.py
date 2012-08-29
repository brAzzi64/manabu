# -*- coding: utf-8 -*-

import sys
import string

from lxml import etree


def get_nodes(n):
    tree = etree.parse( open('kanji.html', 'r') )
    return tree.xpath("//span[@class='c1' and text()]")[:n]

def print_first_kolivas(n):
    nodes = get_nodes(n)
    index = 1
    for node in nodes:
        print u"%d %s" % (index, node.text.strip())
        index += 1

def get_kolivas_mapping():
    nodes = get_nodes(2500)
    mapping = {}
    index = 1
    for node in nodes:
        mapping[node.text.strip()] = index
        index += 1
    return mapping

if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 2500
    print_first_kolivas(n)

