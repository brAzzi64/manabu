from django.db import models

class Kanji(models.Model):
    character = models.CharField(max_length = 1)
    pronunciations = models.ManyToManyField('Pronunciation')
    unicode_index = models.IntegerField()
    kolivas_index = models.IntegerField(null=True)

    def __unicode__(self):
        return "%s (u:%d)" % (self.character, self.unicode_index)

class Pronunciation(models.Model):
    PRONUNCIATION_TYPES = (
        ('ON', "On'yomi"),
        ('KN', "Kun'yomi"),
    )
    ptype = models.CharField(max_length = 2, choices = PRONUNCIATION_TYPES)
    text = models.CharField(max_length = 100)

    def __unicode__(self):
        return self.ptype + " | " + self.text


def get_onyomi_for_kanji(kanji):
    ks = Kanji.objects.filter(character = kanji)
    ps = ks[0].pronunciations.filter(ptype = u'ON')
    return ps

def get_kunyomi_for_kanji(kanji):
    ks = Kanji.objects.filter(character = kanji)
    ps = ks[0].pronunciations.filter(ptype = u'KN')
    return ps

