from django.shortcuts import redirect
from functools import wraps


def onlyuser(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('/signin')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

