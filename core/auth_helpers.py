from .models import Utenti


def get_current_user(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return None
    try:
        return Utenti.objects.get(pk=user_id)
    except Utenti.DoesNotExist:
        del request.session['user_id']
        return None


def set_session_user(request, utente):
    request.session['user_id'] = utente.pk
