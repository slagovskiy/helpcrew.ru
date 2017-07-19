from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.urls import reverse


def authenticate_check(function):
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated:
            return function(request, *args, **kwargs)
        else:
            return redirect(reverse('user_login'))
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
