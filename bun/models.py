# -*- coding: utf-8 -*-
import string
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


class KnownKanji(models.Model):
    """ Temporary entity to store the known Kanji for a user.

    """
    user = models.CharField(max_length = 64)
      # username of the user the array registers the known kanji for (tmp).
    array = models.CharField(max_length = 2136)
      # array with the Jouyou Kanji that are known by the user

    def __unicode__(self):
        return u"for '%s'" % self.user

    # TODO: we won't need this in this way when
    # we handle multiple users in a different way
    @staticmethod
    def get_or_create(username):
        kk = None
        try:
            kk = KnownKanji.objects.get(user = username)
        except KnownKanji.DoesNotExist:
            kk = KnownKanji(user = username)
            kk.save()
        return kk


def get_sentences_with_kanji(kanji):
    return Sentence.objects.get(text__contains = kanji)

