# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.utils import simplejson
from django.http import HttpResponse

from sentence import SentenceGrabber
from restructurer import Restructurer


# global variable
glb = { 'SentenceGrabber' : None }


def ajax_error(message):
    d = { 'error' : message }
    return HttpResponse(simplejson.dumps(d), mimetype = "application/json")

def index(request):
    return render_to_response('index.html')

# bun/train?kanji=X
def train(request):
    k = request.GET.get('kanji', False)
    if not k or len(k) != 1 or not Restructurer.is_kanji(k):
        return ajax_error("GET paramater 'kanji' not found or invalid")
    # create a new instance for kanji k
    glb['SentenceGrabber'] = SentenceGrabber(k)
    return render_to_response('train.html', { 'kanji' : k })

# API for bun/train
def get_next_sentence(request):
    sg = glb['SentenceGrabber']
    bun = sg.pop_next_sentence()
    if bun == None:
        return ajax_error("No more sentences left for this kanji")
    response = { 'sentence' : bun['sentence'], 'structure' : bun['structure'],
                 'structure_orig' : bun['structure_orig'], 'translations' : bun['translations'],
                 'pronunciations' : bun['pronunciations'], 'isLast' : not sg.any_sentence_left() }
    return HttpResponse(simplejson.dumps(response), mimetype = "application/json")

