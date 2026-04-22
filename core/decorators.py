from functools import wraps
from django.shortcuts import redirect, render
from .auth_helpers import get_current_user


def login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not get_current_user(request):
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper


def require_livello(min_livello):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            utente = get_current_user(request)
            if not utente:
                return redirect('login')
            if utente.livello < min_livello:
                return render(request, 'errors/403.html', {
                    'min_livello': min_livello,
                    'livello_utente': utente.livello,
                }, status=403)
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator
