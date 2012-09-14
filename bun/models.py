# -*- coding: utf-8 -*-
from django.db import models

class Sentence(models.Model):
    """ Represents a sentence stored in the DB.

    """
    text = models.CharField(max_length = 1024)
      # the actual sentence
    structure = models.CharField(max_length = 1024)
      # structure, i.e.: 私[わたし] は 忙[いそが]しい 。
    kanji_pronunciations = models.CharField(max_length = 1024)
      # a field in the form: K1:p1,K2:p2,K3:P3...
    learned_date = models.DateTimeField()

    def __unicode__(self):
        return "%s" % (self.text)


def get_sentences_with_kanji(kanji):
    return Sentence.objects.get(text__contains = kanji)

