# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseBadRequest
from django.template import RequestContext
from django.views.decorators.http import require_GET
from django.shortcuts import render_to_response
from django.utils import simplejson

from bun.models import Sentence
from bun.views.common import csrf_ensure_cookie


# URL: review
@csrf_ensure_cookie
@require_GET
def review(request):
    return render_to_response('review.html', { 'section_name': 'Review' }, context_instance = RequestContext(request))

# URL: review/api/get_sentences?page=Y
@require_GET
def get_sentences(request):
    try:
        page = int( request.GET.get('page', '') )
        if page < 0: raise ValueError
    except ValueError:
        return HttpResponseBadRequest("Paramater 'page' is invalid")

    # ignoring the 'page' parameter for now
    sentences = Sentence.objects.filter(user__username = request.user.username).order_by('-learned_date')
    response = []
    for s in sentences:
        elem = { 'date': {
                    'dayAndMonth': "%d %s" % ( s.learned_date.day, s.learned_date.strftime("%B")[:3] ),
                    'year': str(s.learned_date.year)
                 },
                 'sentence' : { 'structure': s.structure, 'translation': s.translation }
               }
        response.append(elem)

    return HttpResponse(simplejson.dumps(response), mimetype = "application/json")


