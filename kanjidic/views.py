# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.utils import simplejson
from django.http import HttpResponse
from kanjidic.models import Kanji

from sentence import SentenceGrabber


sg = SentenceGrabber(u"私")

def index(request):
    sg.get_next_page()
    return render_to_response('kanjidic/index.html')

def kanji(request, kanji):
    try:
        k = Kanji.objects.get(character = kanji)
        onyomis =  [p.text for p in k.pronunciations.all() if p.ptype == u'ON']
        kunyomis = [p.text for p in k.pronunciations.all() if p.ptype == u'KN']
        data = {'character' : k.character, 'onyomis' : onyomis, 'kunyomis' : kunyomis}
    except Kanji.DoesNotExist:
        raise Http404
    return render_to_response('kanjidic/kanji.html', {'kanji' : data})

def get_sentence(request):
    k = request.GET.get('kanji', False)
    d = { 'texto' : sg.sentences[0][0].encode('utf-8') }
    return HttpResponse(simplejson.dumps(d), mimetype = "application/json")

