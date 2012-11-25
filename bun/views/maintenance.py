# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseBadRequest
from django.template import RequestContext
from django.views.decorators.http import require_GET, require_POST
from django.shortcuts import render_to_response, redirect
from django.utils import simplejson
import dateutil.parser

from bun.models import Sentence
from bun.views.common import csrf_ensure_cookie

# these methods don't have a UI. a curl script
# is availible in commands.txt to make use of them.


# URL: maintenance/exportdata
@require_GET
def exportdata(request):
    # get user profile
    up = request.user.get_profile()

    output = u""
    output += u"knownkanji:\n"
    output += up.known_kanji.strip() + u"\n"
    output += u"\n"

    output += u"knownsentences:\n"
    sentences = Sentence.objects.all()
    for s in sentences:
        output += s.learned_date.isoformat() + u"\n"
        output += s.text.strip() + u"\n"
        output += s.structure.strip() + u"\n"
        output += s.kanji_pronunciations.strip() + u"\n"

    response = HttpResponse(output, mimetype = "text/plain; charset=utf-8")
    response['Content-Disposition'] = 'attachment; filename="user-%s.data"' % request.user.username
    return response


# URL: maintenance/importdata
@require_POST
def importdata(request):
    if len( request.FILES.keys() ) > 0:
        file = request.FILES[ request.FILES.keys()[0] ]
        lines = file.readlines()

        #TODO: validate file format

        # write known kanji
        known_kanji = lines[1].decode('utf-8')
        up = request.user.get_profile()
        up.known_kanji = known_kanji
        up.save()
        i = 4

        # erase existing sentences
        Sentence.objects.all().delete()

        # read sentences
        try:
            while True:
                date = dateutil.parser.parse( lines[i].decode('utf-8') )
                text = lines[i+1].decode('utf-8')
                structure = lines[i+2].decode('utf-8')
                pronunciations = lines[i+3].decode('utf-8')

                s = Sentence(user = request.user, text = text, structure = structure,
                             learned_date = date, kanji_pronunciations = pronunciations)
                s.save()

                i += 4
        except IndexError:
            # finished processing the file
            pass

    return HttpResponse()

