# -*- coding: utf-8 -*-
import string
import datetime

from django.shortcuts import render_to_response
from django.utils import simplejson
from django.http import HttpResponse
from django.template import RequestContext, Context, loader

from bun.models import Sentence
from sentence import SentenceGrabber
from restructurer import Restructurer


# global variable
glb = { 'SentenceGrabber' : None }


def ajax_error(message):
    d = { 'error' : message }
    return HttpResponse(simplejson.dumps(d), mimetype = "application/json")

def index(request):
    return render_to_response('index.html')

# GET | bun/train?kanji=X
def train(request):
    k = request.GET.get('kanji', False)
    if not k or len(k) != 1 or not Restructurer.is_kanji(k):
        return ajax_error("GET paramater 'kanji' not found or invalid")
    # create a new instance for kanji k
    glb['SentenceGrabber'] = SentenceGrabber(k)
    return render_to_response('train.html', { 'kanji' : k }, context_instance = RequestContext(request))

#
# API for bun/train

# GET | no params
def get_next_sentence(request):
    sg = glb['SentenceGrabber']
    bun = sg.pop_next_sentence()
    if bun == None:
        return ajax_error("No more sentences left for this kanji")
    response = { 'sentence' : bun['sentence'], 'structure' : bun['structure'],
                 'structure_orig' : bun['structure_orig'], 'translations' : bun['translations'],
                 'pronunciations' : bun['pronunciations'], 'isLast' : not sg.any_sentence_left() }
    return HttpResponse(simplejson.dumps(response), mimetype = "application/json")

# POST | params: text, structure, pronunciations
def learn_sentence(request):
    text = request.POST.get('text', False)
    structure = request.POST.get('structure', False)
    pronunciations = request.POST.get('pronunciations', False)

    # convert to the DB storing format
    prs_dict = simplejson.loads(pronunciations)
    prs_string = string.join((u"%s:%s" % (k,v) for (k,v) in prs_dict.items()), ",")

    s = Sentence(text = text, structure = structure, learned_date = datetime.datetime.now(), kanji_pronunciations = prs_string)
    s.save()

    return HttpResponse(simplejson.dumps({ 'result' : 'ok' }), mimetype = "application/json")


# GET | bun/review
def review(request):
    sentences = Sentence.objects.all()
    t = loader.get_template('review.html')
    c = Context({ 'sentences' : sentences })
    return HttpResponse(t.render(c))

