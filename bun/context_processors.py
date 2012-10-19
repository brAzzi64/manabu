

def default(request):
    if request.user.is_authenticated():
        user = request.user.username
    else:
        user = 'guest'
    return dict( username = user)

