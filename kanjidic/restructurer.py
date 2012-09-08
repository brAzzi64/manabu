# -*- coding: utf-8 -*-
import re
import string

class Restructurer():
    """
    Receives a string with the structure of a sentence
    in Tatoeba's format and converts it to ours. Ex:

      in:  私[わたし] は 忙しい[いそがしい] 。
      out: 私[わたし] は 忙[いそが]しい 。
    """
    @staticmethod
    def is_kanji(char):
        return ord(char) >= 0x4E00 and ord(char) < 0x9FFF

    @staticmethod
    def is_kanji_or_iteration(char):
        return Restructurer.is_kanji(char) or char == u'々'

    @staticmethod
    def is_kana(char):
        return ord(char) >= 0x3040 and ord(char) < 0x309F \
            or ord(char) >= 0x30A0 and ord(char) < 0x30FF

    def build_new_struct(self, word, pronunciation):
        output = u""
        kanji_list = list(x for x in word if not self.is_kana(x))
        if len(kanji_list) == 0:
            output += u"%s[%s]" % (word, pronunciation)
            print "WARNING: There should be at least a non-kana character"
        else:
            # build regular expression
            replace = lambda x: '(.*)' if not self.is_kana(x) else x
            regexp_str = string.join( [replace(i) for i in word], "" )

            # match pronunciation against it        
            match = re.match(regexp_str, pronunciation)
            if match != None:
                groups = [g for g in match.groups() if g != ""]
                g_index = 0
                for i, l in enumerate(word):
                    if self.is_kana(l):
                        output += l
                    else: # is kanji
                        # if next char is also kanji, we know that both
                        # are matched in the same group
                        if len(word) > i + 1 and not self.is_kana( word[i+1] ):
                            output += l
                        else:
                            output += u"%s[%s]" % (l, groups[g_index])
                            g_index += 1
            else:
                error = u"Word '%s' doesn't match pronunciation '%s' with '%s'" % (word, pronunciation, regexp_str)
                print error
                raise Exception(error)
        return output

    def feed(self, struct):
        out = []
        words = struct.split(" ")
        for w in words:
            match = re.match("(.*)\[(.*)\]", w)
            if not match:
                out.append(w)
            else:
                wrd = match.groups()[0]
                pro = match.groups()[1]
                #print u"W: %s - P: %s" % (wrd, pro)
                m = self.build_new_struct(wrd, pro)
                out.append(m)
                #print u"struct: %s" % m
        return string.join(out, " ")


if __name__ == '__main__':
    r = Restructurer()
    struct = u"彼女[かのじょ] は 今日[きょう] 、 お弁当[おべんとう] を 持っ[もっ] て 来[き] た 。"
    print u"original: %s" % struct
    print u"adjusted: %s" % r.feed(struct)

    struct = u"知り合い[しりあい] 。"
    print u"original: %s" % struct
    print u"adjusted: %s" % r.feed(struct)

    struct = u"友ば達働いて便足知り異馬[ぼばもとにいてかりもすこ] 。"
    print u"original: %s" % struct
    print u"adjusted: %s" % r.feed(struct)

