# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.utils import simplejson
from django.http import HttpResponse
from kanjidic.models import Kanji

from sentence import SentenceGrabber


# global variable
glb = { 'SentenceGrabber' : None }


def ajax_error(message):
    d = { 'error' : message }
    return HttpResponse(simplejson.dumps(d), mimetype = "application/json")

def generate_sentence_response(bun):
    return { 'sentence' : bun['sentence'],
             'structure' : bun['structure'],
             'structure_orig' : bun['structure_orig'],
             'translations' : bun['translations'],
             'pronunciations' : bun['pronunciations'],
             'isLast' : not glb['SentenceGrabber'].any_sentence_left() }


def index(request):
    return render_to_response('kanjidic/index.html')

def get_sentence_begin(request):
    k = request.GET.get('kanji', False)
    if not k:
        return ajax_error("GET paramater 'kanji' not found or invalid")
    # create a new instance for kanji k
    glb['SentenceGrabber'] = SentenceGrabber(k)
    # wait for the first sentence
    bun = glb['SentenceGrabber'].pop_next_sentence()
    if bun == None:
        return ajax_error("No sentences for this kanji")
    response = generate_sentence_response(bun)
    return HttpResponse(simplejson.dumps(response), mimetype = "application/json")

def get_sentence_next(request):
    bun = glb['SentenceGrabber'].pop_next_sentence()
    if bun == None:
        return ajax_error("No more sentences left for this kanji")
    response = generate_sentence_response(bun)
    return HttpResponse(simplejson.dumps(response), mimetype = "application/json")


# USELESS, JUST FOR THE RECORD
def kanji(request, kanji):
    try:
        k = Kanji.objects.get(character = kanji)
        onyomis =  [p.text for p in k.pronunciations.all() if p.ptype == u'ON']
        kunyomis = [p.text for p in k.pronunciations.all() if p.ptype == u'KN']
        data = {'character' : k.character, 'onyomis' : onyomis, 'kunyomis' : kunyomis}
    except Kanji.DoesNotExist:
        raise Http404
    return render_to_response('kanjidic/kanji.html', {'kanji' : data})

