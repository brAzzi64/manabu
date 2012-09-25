# -*- coding: utf-8 -*-

# setup the environment
from django.core.management import setup_environ
import settings

setup_environ(settings)

# script start
import string

from optparse import OptionParser

from bun.jishopar import JishoParser
from bun.tatopar import TatoebaParser
from bun.restructurer import Restructurer
from bun.kanjidic import KanjiDic, Kanji
from bun.models import ScrapedSentence


# run from /other folder with:
# PYTHONPATH=`pwd`/.. python export_sentences_db.py
if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-o", "--output-file", dest = "outputfile")
    (options, args) = parser.parse_args()

    f = open(options.outputfile, "w")
    for ss in ScrapedSentence.objects.all():
        f.write( (u"%s;%s;%s\n" % (ss.text, ss.structure, ss.translations)).encode("utf-8") )
    f.close()

