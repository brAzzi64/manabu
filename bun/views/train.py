# -*- coding: utf-8 -*-
import string
import datetime
import re

from django.utils import simplejson
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render_to_response
from django.views.decorators.http import require_GET, require_POST
from django.template import RequestContext, Context, loader

from bun.models import Sentence
from bun.views.common import csrf_ensure_cookie
from bun.restructurer import Restructurer
from bun.kanjidic import Kanji, KanjiDic
from bun.sentenceprovider import FileSentenceProvider


# URL: train
@csrf_ensure_cookie
@require_GET
def train(request):
    return render_to_response('train.html', { 'section_name': 'Train' }, context_instance = RequestContext(request))


# URL: train/api/get_sentences?kanji=X&page=Y
@require_GET
def get_sentences(request):
    kanji = request.GET.get('kanji', False)
    if not kanji or len(kanji) != 1 or not Restructurer.is_kanji(kanji):
        return HttpResponseBadRequest("Paramater 'kanji' is invalid")
    try:
        page = int( request.GET.get('page', '') )
        if page < 0: raise ValueError
    except ValueError:
        return HttpResponseBadRequest("Paramater 'page' is invalid")

    up = request.user.get_profile()
    sp = FileSentenceProvider()
    ss = sp.get_sentences(kanji, 1, page, up.known_kanji) # hardcoding items_per_page to 1 for now
    if not ss:
        return HttpResponseBadRequest("No sentences left for kanji '%s' in page %d" % (kanji, page))

    sentences = []
    for bun in ss:
        sentences.append( { 'sentence' : bun[0],
                            'structure' : bun[1],
                            'translations' : bun[2],
                            'pronunciations' : get_pronunciations( bun[0] ) } )

    return HttpResponse(simplejson.dumps(sentences), mimetype = "application/json")


def get_pronunciations(sentence):
    kc = KanjiDic()
    mappings = {}
    kanjis = set(l for l in sentence if Restructurer.is_kanji(l))
    for literal in kanjis:
        onyomis = []
        kunyomis = []
        try:
            kanji = kc[literal]
            onyomis = list(kanji.onyomis)
            kunyomis = list(kanji.kunyomis)
        except Exception as e:
            print u"No information for Kanji: %s" % literal
            print e
        mappings[literal] = { 'ON' : onyomis, 'KN' : kunyomis }
    return mappings


# URL: train/api/learn_sentence
# PARAMS: text, structure, pronunciations
@require_POST
def learn_sentence(request):
    text = request.POST.get('text', False)
    structure = request.POST.get('structure', False)
    pronunciations = request.POST.get('pronunciations', False)
    if not (text and structure and pronunciations):
        return HttpResponseBadRequest("Parameters 'text', 'structure' and 'pronunciations' not found or invalid")

    # convert to the DB storing format
    prs_dict = simplejson.loads(pronunciations)
    prs_string = string.join((u"%s:%s" % (k,v) for (k,v) in prs_dict.items()), ",")

    s = Sentence(user = request.user, text = text, structure = structure, learned_date = datetime.datetime.now(), kanji_pronunciations = prs_string)
    s.save()

    return HttpResponse()


import urllib

class UserAgentOpener(urllib.FancyURLopener):
    version = "Mozilla/4.0 (MSIE 6.0; Windows NT 5.0)2011-03-10 15:38:34"

# URL: train/api/get_audio?text=X
@require_GET
def get_audio(request):
    text = request.GET.get('text', False)
    if not text:
        return HttpResponseBadRequest("Parameter 'text' not found or invalid")

    urlencoded_text = urllib.quote( text.encode('utf-8') )
    languageCode = 'ja'

    url = "http://translate.google.com/translate_tts?tl=%s&q=%s" % (languageCode, urllib.quote(urlencoded_text))
    opener = UserAgentOpener()
    data = opener.open(url, 'rb').read()

    return HttpResponse(data, mimetype="audio/mpeg")

