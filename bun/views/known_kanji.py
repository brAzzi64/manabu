# -*- coding: utf-8 -*-
import string
import re

from django.utils import simplejson
from django.http import HttpResponse, HttpResponseBadRequest
from django.template import RequestContext, Context, loader
from django.shortcuts import render_to_response
from django.views.decorators.http import require_GET, require_POST

from bun.views.common import csrf_ensure_cookie
from bun.kanjidic import Kanji, KanjiDic
from bun.sentenceprovider import FileSentenceProvider


# URL: known_kanji
@csrf_ensure_cookie
@require_GET
def known_kanji(request):
    return render_to_response('known_kanji.html', { 'section_name': 'Known Kanji' }, context_instance = RequestContext(request))


# URL: known_kanji/api/get_kanji?page=X
@require_GET
def get_kanji(request):
    try:
        page = int( request.GET.get('page', '') )
        if page < 0: raise ValueError
    except ValueError:
        # page 0 if parameter is invalid or missing
        page = 0

    kd = KanjiDic()
    d = []
    # assuming there's an authenticated user
    up = request.user.get_profile()
    for k in kd.keys():
        idx_unicode = kd[k].idx_unicode
        idx_unisort = kd[k].idx_unisort
        # all of the Kanji in kd are Jouyou right no
        known = k in up.known_kanji
        entry = { 'literal': k, 'known': known }
        d.append(entry)

    # return them ordered by unisort index
    d = sorted(d, key = lambda x: kd[ x['literal'] ].idx_kolivas)

    kanji_per_page = 96
    start = page * kanji_per_page
    end = start + kanji_per_page
    response = d[start:end]

    return HttpResponse(simplejson.dumps(response), mimetype = "application/json")


# URL: known_kanji/api/update_known_kanji
# PARAMS: updates
@require_POST
def update_known_kanji(request):
    updates = request.POST.get('updates', False)
    if updates == None:
        return HttpResponseBadRequest("Parameter 'updates' not found or invalid")

    # assuming there's an authenticated user
    up = request.user.get_profile()
    kd = KanjiDic()
    d = simplejson.loads(updates)
    learned = string.join((k[u"literal"] for k in d if k[u"known"]), u"")
    unlearned = string.join((k[u"literal"] for k in d if not k[u"known"]), u"")
    # we put the random symbol 'k' to avoid changes
    # in the logic when we have no unlearned kanji
    up.known_kanji = re.sub(u'[k%s]' % unlearned, '', up.known_kanji) + learned
    up.save()

    # clear the cache for the learned kanjis
    sp = FileSentenceProvider()
    sp.clear_cache()

    return HttpResponse()


