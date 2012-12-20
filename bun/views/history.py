# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseBadRequest
from django.template import RequestContext
from django.views.decorators.http import require_GET
from django.shortcuts import render_to_response
from django.utils import simplejson

from bun.models import Sentence
from bun.views.common import csrf_ensure_cookie


# URL: history
@csrf_ensure_cookie
@require_GET
def history(request):
    return render_to_response('history.html', { 'section_name': 'History' }, context_instance = RequestContext(request))

# URL: history/api/get_sentences?page=Y
@require_GET
def get_sentences(request):
    try:
        page = int( request.GET.get('page', '') )
        if page < 0: raise ValueError
    except ValueError:
        return HttpResponseBadRequest("Paramater 'page' is invalid")

    # ignoring the 'page' parameter for now
    sentences = Sentence.objects.filter(user__username = request.user.username).order_by('-learned_date')
    response = {}
    for s in sentences:
        date = "%s %d, %d" % ( s.learned_date.strftime("%B"), s.learned_date.day, s.learned_date.year )
        try:
            lst = response[date]
        except KeyError:
            lst = []
            response[date] = lst
        lst.append({ 'structure': s.structure, 'translation': s.translation })

    return HttpResponse(simplejson.dumps(response), mimetype = "application/json")


