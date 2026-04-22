from django.db.models import Count


def check_and_promote(utente, evento):
    """
    Promuove l'utente in base ai contributi.
    evento: 'commento' | 'articolo' | 'attacco'
    """
    if evento == 'commento':
        from core.models import Interazione
        n_commenti = Interazione.objects.filter(
            id_utente=utente, tipo='commento'
        ).count()
        bonus = n_commenti // 3
        livello_target = bonus
        if utente.livello < livello_target:
            utente.livello = livello_target
            utente.save(update_fields=['livello'])

    elif evento == 'articolo':
        from core.models import Articolo
        n_articoli = Articolo.objects.filter(id_autore=utente).count()
        bonus = n_articoli
        if utente.livello < bonus:
            utente.livello = bonus
            utente.save(update_fields=['livello'])

    elif evento == 'attacco':
        from core.models import Attacco
        n_attacchi = Attacco.objects.filter(id_autore=utente).count()
        bonus = n_attacchi * 2
        if utente.livello < bonus:
            utente.livello = bonus
            utente.save(update_fields=['livello'])
