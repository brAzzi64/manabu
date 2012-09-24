# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.template import Context, loader
from django.views.decorators.http import require_GET

from bun.models import Sentence
from bun.views.common import csrf_ensure_cookie


# URL: review
@csrf_ensure_cookie
@require_GET
def review(request):
    sentences = Sentence.objects.order_by('-learned_date')
    t = loader.get_template('review.html')
    c = Context({ 'section_name': 'Review', 'sentences': sentences })
    return HttpResponse(t.render(c))

