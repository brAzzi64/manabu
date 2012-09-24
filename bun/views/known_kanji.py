# -*- coding: utf-8 -*-
import string
import re

from django.utils import simplejson
from django.http import HttpResponse, HttpResponseBadRequest
from django.template import Context, loader
from django.views.decorators.http import require_GET, require_POST

from bun.models import KnownKanji
from bun.views.common import csrf_ensure_cookie
from bun.kanjidic import Kanji, KanjiDic

# global variable
glb = { 'KnownKanji' : None }
# get or initialize the KnownKanji object
glb['KnownKanji'] = KnownKanji.get_or_create('brazzi')



# URL: known_kanji
@csrf_ensure_cookie
@require_GET
def known_kanji(request):
    kd = KanjiDic()
    d = []
    kk = glb['KnownKanji']
    known_kanji = kk.array
    for k in kd.keys():
        idx_unicode = kd[k].idx_unicode
        idx_unisort = kd[k].idx_unisort
        # all of the Kanji in kd are Jouyou right no
        known = k in known_kanji
        entry = { 'literal': k, 'known': known }
        d.append(entry)

    # return them ordered by unisort index
    d = sorted(d, key = lambda x: kd[ x['literal'] ].idx_kolivas)

    t = loader.get_template('known_kanji.html')
    c = Context({ 'section_name': 'Known Kanji', 'kanjis': d })
    return HttpResponse(t.render(c))


# URL: known_kanji/api/update_known_kanji
# PARAMS: updates
@require_POST
def update_known_kanji(request):
    updates = request.POST.get('updates', False)
    if updates == None:
        return HttpResponseBadRequest("Parameter 'updates' not found or invalid")

    kd = KanjiDic()
    kk = glb['KnownKanji']
    d = simplejson.loads(updates)
    learned = string.join((k for k in d if d[k]), u"")
    unlearned = string.join((k for k in d if not d[k]), u"")
    # we put the random symbol 'k' to avoid changes
    # in the logic when we have no unlearned kanji
    kk.array = re.sub(u'[k%s]' % unlearned, '', kk.array) + learned
    kk.save()

    return HttpResponse()


