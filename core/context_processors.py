from .models import Utenti


def current_user(request):
    user_id = request.session.get('user_id')
    if user_id:
        try:
            return {'utente_corrente': Utenti.objects.get(pk=user_id)}
        except Utenti.DoesNotExist:
            del request.session['user_id']
    return {'utente_corrente': None}
