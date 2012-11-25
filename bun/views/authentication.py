# -*- coding: utf-8 -*-
import string
import datetime
import re

from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.views.decorators.http import require_GET, require_POST
import django.contrib.auth as django_auth
from django.shortcuts import redirect


# URL: login?user=X&pass=Y
@require_GET
def login(request):
    usr = request.GET.get('user', False)
    if not usr or len(usr) == 0:
        return HttpResponseBadRequest("Paramater 'user' is invalid")
    pwd = request.GET.get('pass', False)
    if not pwd or len(pwd) == 0:
        return HttpResponseBadRequest("Paramater 'pass' is invalid")

    if not request.user.is_authenticated():
        user = django_auth.authenticate(username = usr, password = pwd)
        if user is not None:
            django_auth.login(request, user)
            # user logged in successfully
            return HttpResponseRedirect('/bun')
        else:
            return HttpResponseBadRequest("Invalid login")
    else:
        return HttpResponseBadRequest("User was already authenticated")


# URL: logout
@require_GET
def logout(request):
    django_auth.logout(request)
    return HttpResponse("User logged out successfully")


#URL: /
@require_GET
def start(request):
    # login in the testuser by default if no other is logged in
    if not request.user.is_authenticated():
        user = django_auth.authenticate(username = 'testuser', password = 'testpassword')
        if user is not None:
            django_auth.login(request, user)

    return redirect('/bun/train')


