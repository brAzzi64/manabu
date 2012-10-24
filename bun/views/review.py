# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.template import RequestContext
from django.views.decorators.http import require_GET
from django.shortcuts import render_to_response

from bun.models import Sentence
from bun.views.common import csrf_ensure_cookie


# URL: review
@csrf_ensure_cookie
@require_GET
def review(request):
    sentences = Sentence.objects.order_by('-learned_date')
    return render_to_response('review.html', { 'section_name': 'Review', 'sentences': sentences }, context_instance = RequestContext(request))

