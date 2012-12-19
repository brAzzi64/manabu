# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.template import RequestContext
from django.views.decorators.http import require_GET
from django.shortcuts import render_to_response
from django.utils import simplejson
from random import Random

from bun.models import Sentence
from bun.views.common import csrf_ensure_cookie


# URL: review
@csrf_ensure_cookie
@require_GET
def review(request):
    return render_to_response('review.html', { 'section_name': 'Review' }, context_instance = RequestContext(request))

# URL: review/api/get_random_sentence
@require_GET
def get_random_sentence(request):
    r = Random()
    sentence_count = Sentence.objects.filter(user__username = request.user.username).count()
    random_idx = r.randrange(0, sentence_count)
    s = Sentence.objects.filter(user__username = request.user.username)[random_idx:random_idx+1]
    s = s[0] # take only one element from the set

    response = { 'structure': s.structure, 'translation': s.translation }

    return HttpResponse(simplejson.dumps(response), mimetype = "application/json")


