from django.http import HttpResponse
from django.shortcuts import redirect


def authenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func


def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('index')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func

