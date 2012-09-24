from functools import wraps
from django.utils.decorators import available_attrs


# the following decorator is present on Django 1.3 but not in 1.4
def csrf_ensure_cookie(view_func):
    """
    Ensures that the CSRF cookie is sent to the client, regardless of whether
    we use it to generate a response.
    """
    def wrapped_view(request, *args, **kwargs):
        request.META["CSRF_COOKIE_USED"] = True
        return view_func(request, *args, **kwargs)
    return wraps(view_func, assigned=available_attrs(view_func))(wrapped_view)

