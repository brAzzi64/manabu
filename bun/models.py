# -*- coding: utf-8 -*-
import string
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class UserProfile(models.Model):
    """ Asociate basic data to a User.

    """
    # foreign key to User
    user = models.OneToOneField(User)

    # actual fields
    known_kanji = models.CharField(max_length = 2136)
    # array with the Jouyou Kanji that are known by the user

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user = instance)

post_save.connect(create_user_profile, sender = User)


class Sentence(models.Model):
    """ Represents a sentence stored in the DB.

    """
    # foreign key to User
    user = models.ForeignKey(User)

    # the actual sentence
    text = models.CharField(max_length = 1024)

    # structure, i.e.: 私[わたし] は 忙[いそが]しい 。
    structure = models.CharField(max_length = 1024)

    # a field in the form: K1:p1,K2:p2,K3:P3...
    kanji_pronunciations = models.CharField(max_length = 1024)

    # the meaning of the sentence
    translation = models.CharField(max_length = 1024)

    learned_date = models.DateTimeField()

    def __unicode__(self):
        return "%s" % (self.text)


class ScrapedSentence(models.Model):
    """ Represents a scraped sentence stored in the DB.

    """
    text = models.CharField(max_length = 4096)
      # the actual sentence
    structure = models.CharField(max_length = 4096)
      # structure, i.e.: 私[わたし] は 忙[いそが]しい 。
    orig_structure = models.CharField(max_length = 4096)
      # structure, as it comes from the source.
    translations = models.CharField(max_length = 4094)
      # a field in the form: t1|t1|t3...

    def __unicode__(self):
        return "%s" % (self.text)


