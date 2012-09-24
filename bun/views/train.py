# -*- coding: utf-8 -*-
import string
import datetime
import re

from django.utils import simplejson
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render_to_response
from django.views.decorators.http import require_GET, require_POST
from django.template import RequestContext, Context, loader

from bun.models import Sentence, KnownKanji
from bun.views.common import csrf_ensure_cookie
from bun.sentence import SentenceGrabber
from bun.restructurer import Restructurer


# global variable
glb = { 'SentenceGrabber' : None, 'KnownKanji' : None }
# get or initialize the KnownKanji object
glb['KnownKanji'] = KnownKanji.get_or_create('brazzi')

# TODO: RESTful API

# URL: train?kanji=X
@csrf_ensure_cookie
@require_GET
def train(request):
    kanji = request.GET.get('kanji', False)
    # if no parameters, return search page
    if not kanji:
        return render_to_response('search.html', { 'section_name': 'Search' })

    if len(kanji) != 1 or not Restructurer.is_kanji(kanji):
        return HttpResponseBadRequest("Paramater 'kanji' is invalid")

    # create a new instance for kanji k
    glb['SentenceGrabber'] = SentenceGrabber(kanji, glb['KnownKanji'].array)
    return render_to_response('train.html', { 'section_name': 'Train', 'kanji': kanji }, context_instance = RequestContext(request))


# URL: train/api/get_next_sentence
@require_GET
def get_next_sentence(request):
    sg = glb['SentenceGrabber']
    bun = sg.pop_next_sentence()
    if bun == None:
        return HTTPResponseBadRequest("No more sentences left for this kanji")

    response = { 'sentence' : bun['sentence'], 'structure' : bun['structure'],
                 'structure_orig' : bun['structure_orig'], 'translations' : bun['translations'],
                 'pronunciations' : bun['pronunciations'], 'isLast' : not sg.any_sentence_left() }

    return HttpResponse(simplejson.dumps(response), mimetype = "application/json")


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

    s = Sentence(text = text, structure = structure, learned_date = datetime.datetime.now(), kanji_pronunciations = prs_string)
    s.save()

    return HttpResponse()


