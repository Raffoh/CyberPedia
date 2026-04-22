from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST, require_GET
from django.db import transaction, connection
from django.core.paginator import Paginator
from django.utils import timezone
from django.contrib import messages

from .models import (
    Utenti, Attacco, AttaccoRete, AttaccoWeb, AttaccoSocial, AttaccoMalware,
    Vulnerabilita, Contromisura, CasoReale, Articolo,
    Interazione, InterazioneAttacco, InterazioneArticolo, InterazioneCaso,
    Sfrutta, Mitiga, Seguito,
)
from .forms import (
    RegistrazioneForm, LoginForm,
    AttaccoBaseForm, AttaccoReteForm, AttaccoWebForm,
    AttaccoSocialForm, AttaccoMalwareForm,
    VulnerabilitaForm, ContromisuraForm, CasoRealeForm,
    ArticoloForm, ProfiloForm,
)
from .decorators import login_required, require_livello
from .auth_helpers import get_current_user, set_session_user
from .services.leveling import check_and_promote


# ===========================================================================
# HOME
# ===========================================================================

def home_feed(request):
    utente = get_current_user(request)
    if utente:
        following_ids = Seguito.objects.filter(
            id_seguace=utente
        ).values_list('id_utente_seguito_id', flat=True)
        attacchi_feed = Attacco.objects.filter(
            id_autore_id__in=following_ids
        ).select_related('id_autore').order_by('-data_pubblicazione')[:10]
        articoli_feed = Articolo.objects.filter(
            id_autore_id__in=following_ids
        ).select_related('id_autore').order_by('-data_pubblicazione')[:5]
    else:
        attacchi_feed = Attacco.objects.select_related('id_autore').order_by('-data_pubblicazione')[:10]
        articoli_feed = Articolo.objects.select_related('id_autore').order_by('-data_pubblicazione')[:5]

    return render(request, 'home.html', {
        'attacchi_feed': attacchi_feed,
        'articoli_feed': articoli_feed,
    })


# ===========================================================================
# AUTH
# ===========================================================================

def register_view(request):
    if get_current_user(request):
        return redirect('home')
    if request.method == 'POST':
        form = RegistrazioneForm(request.POST)
        if form.is_valid():
            utente = Utenti(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
            )
            from django.contrib.auth.hashers import make_password
            utente.password = make_password(form.cleaned_data['password1'])
            utente.save()
            set_session_user(request, utente)
            messages.success(request, 'Registrazione completata. Benvenuto!')
            return redirect('home')
    else:
        form = RegistrazioneForm()
    return render(request, 'auth/register.html', {'form': form})


def login_view(request):
    if get_current_user(request):
        return redirect('home')

    lockout_until = request.session.get('lockout_until')
    if lockout_until:
        from datetime import datetime
        if datetime.fromisoformat(lockout_until) > datetime.now():
            return render(request, 'auth/login.html', {
                'form': LoginForm(),
                'lockout': True,
            })
        else:
            del request.session['lockout_until']
            request.session['login_attempts'] = 0

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            try:
                utente = Utenti.objects.get(username=username)
                from django.contrib.auth.hashers import check_password
                if check_password(password, utente.password):
                    request.session['login_attempts'] = 0
                    set_session_user(request, utente)
                    messages.success(request, f'Bentornato, {utente.username}!')
                    return redirect('home')
                else:
                    raise Utenti.DoesNotExist
            except Utenti.DoesNotExist:
                attempts = request.session.get('login_attempts', 0) + 1
                request.session['login_attempts'] = attempts
                if attempts >= 3:
                    from datetime import datetime, timedelta
                    lockout = datetime.now() + timedelta(minutes=15)
                    request.session['lockout_until'] = lockout.isoformat()
                    form.add_error(None, 'Troppi tentativi. Account bloccato per 15 minuti.')
                else:
                    form.add_error(None, f'Credenziali errate. Tentativi rimasti: {3 - attempts}')
    else:
        form = LoginForm()
    return render(request, 'auth/login.html', {'form': form, 'lockout': False})


def logout_view(request):
    request.session.flush()
    messages.info(request, 'Disconnesso con successo.')
    return redirect('home')


# ===========================================================================
# ATTACCHI
# ===========================================================================

def attacchi_list(request):
    famiglia = request.GET.get('famiglia', '')
    severita = request.GET.get('severita', '')
    qs = Attacco.objects.select_related('id_autore').order_by('-data_pubblicazione')
    if famiglia == 'rete':
        qs = qs.filter(rete__isnull=False)
    elif famiglia == 'web':
        qs = qs.filter(web__isnull=False)
    elif famiglia == 'social':
        qs = qs.filter(social__isnull=False)
    elif famiglia == 'malware':
        qs = qs.filter(malware__isnull=False)
    if severita:
        qs = qs.filter(severita=severita)

    paginator = Paginator(qs, 12)
    page = paginator.get_page(request.GET.get('page'))
    return render(request, 'attacchi/list.html', {
        'page_obj': page,
        'famiglia': famiglia,
        'severita': severita,
    })


def attacco_detail(request, pk):
    attacco = get_object_or_404(
        Attacco.objects.select_related('id_autore'),
        pk=pk
    )
    vulnerabilita = Vulnerabilita.objects.filter(sfrutta__id_attacco=attacco)
    contromisure = Mitiga.objects.filter(
        id_attacco=attacco
    ).select_related('id_contromisura')
    casi = CasoReale.objects.filter(id_attacco=attacco).order_by('-anno')
    commenti = InterazioneAttacco.objects.filter(
        id_attacco=attacco,
        interazione__tipo='commento'
    ).select_related('interazione__id_utente').order_by('-interazione__data')
    n_like = InterazioneAttacco.objects.filter(
        id_attacco=attacco, interazione__tipo='like'
    ).count()

    utente = get_current_user(request)
    ha_messo_like = False
    if utente:
        ha_messo_like = InterazioneAttacco.objects.filter(
            id_attacco=attacco,
            interazione__tipo='like',
            interazione__id_utente=utente,
        ).exists()

    sottoclasse = None
    for attr in ('rete', 'web', 'social', 'malware'):
        if hasattr(attacco, attr):
            try:
                sottoclasse = (attr, getattr(attacco, attr))
                break
            except Exception:
                pass

    return render(request, 'attacchi/detail.html', {
        'attacco': attacco,
        'sottoclasse': sottoclasse,
        'vulnerabilita': vulnerabilita,
        'contromisure': contromisure,
        'casi': casi,
        'commenti': commenti,
        'n_like': n_like,
        'ha_messo_like': ha_messo_like,
    })


@login_required
@require_livello(10)
def attacco_create(request):
    tipo = request.POST.get('tipo') or request.GET.get('tipo', 'rete')
    TIPO_FORM = {
        'rete': AttaccoReteForm,
        'web': AttaccoWebForm,
        'social': AttaccoSocialForm,
        'malware': AttaccoMalwareForm,
    }
    SubForm = TIPO_FORM.get(tipo, AttaccoReteForm)

    if request.method == 'POST':
        base_form = AttaccoBaseForm(request.POST, request.FILES)
        sub_form = SubForm(request.POST)
        if base_form.is_valid() and sub_form.is_valid():
            with transaction.atomic():
                attacco = base_form.save(commit=False)
                attacco.id_autore = get_current_user(request)
                attacco.save()
                sub = sub_form.save(commit=False)
                sub.attacco = attacco
                sub.save()
            check_and_promote(get_current_user(request), 'attacco')
            messages.success(request, 'Attacco pubblicato con successo.')
            return redirect('attacco-detail', pk=attacco.pk)
    else:
        base_form = AttaccoBaseForm()
        sub_form = SubForm()

    return render(request, 'attacchi/form.html', {
        'base_form': base_form,
        'sub_form': sub_form,
        'tipo': tipo,
        'tipi': ['rete', 'web', 'social', 'malware'],
        'azione': 'Crea',
    })


@login_required
def attacco_edit(request, pk):
    attacco = get_object_or_404(Attacco, pk=pk)
    utente = get_current_user(request)
    if attacco.id_autore != utente and utente.livello < 20:
        return render(request, 'errors/403.html', status=403)

    tipo = attacco.get_famiglia()
    TIPO_MAP = {
        'rete': (AttaccoReteForm, lambda a: a.rete),
        'web': (AttaccoWebForm, lambda a: a.web),
        'social': (AttaccoSocialForm, lambda a: a.social),
        'malware': (AttaccoMalwareForm, lambda a: a.malware),
    }
    SubForm, get_sub = TIPO_MAP.get(tipo, (AttaccoReteForm, lambda a: None))
    sub_instance = get_sub(attacco) if tipo != 'sconosciuta' else None

    if request.method == 'POST':
        base_form = AttaccoBaseForm(request.POST, request.FILES, instance=attacco)
        sub_form = SubForm(request.POST, instance=sub_instance)
        if base_form.is_valid() and sub_form.is_valid():
            with transaction.atomic():
                base_form.save()
                sub_form.save()
            messages.success(request, 'Attacco aggiornato.')
            return redirect('attacco-detail', pk=pk)
    else:
        base_form = AttaccoBaseForm(instance=attacco)
        sub_form = SubForm(instance=sub_instance)

    return render(request, 'attacchi/form.html', {
        'base_form': base_form,
        'sub_form': sub_form,
        'tipo': tipo,
        'tipi': ['rete', 'web', 'social', 'malware'],
        'azione': 'Modifica',
        'attacco': attacco,
    })


@login_required
@require_POST
def attacco_delete(request, pk):
    attacco = get_object_or_404(Attacco, pk=pk)
    utente = get_current_user(request)
    if attacco.id_autore != utente and utente.livello < 20:
        return render(request, 'errors/403.html', status=403)
    attacco.delete()
    messages.success(request, 'Attacco eliminato.')
    return redirect('attacchi-list')


# ===========================================================================
# VULNERABILITA
# ===========================================================================

def vulnerabilita_list(request):
    qs = Vulnerabilita.objects.order_by('-anno_scoperta')
    paginator = Paginator(qs, 15)
    page = paginator.get_page(request.GET.get('page'))
    return render(request, 'vulnerabilita/list.html', {'page_obj': page})


def vulnerabilita_detail(request, pk):
    vuln = get_object_or_404(Vulnerabilita, pk=pk)
    attacchi = Attacco.objects.filter(sfrutta__id_vulnerabilita=vuln).select_related('id_autore')
    return render(request, 'vulnerabilita/detail.html', {
        'vuln': vuln,
        'attacchi': attacchi,
    })


@login_required
@require_livello(5)
def vulnerabilita_create(request):
    if request.method == 'POST':
        form = VulnerabilitaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Vulnerabilità aggiunta.')
            return redirect('vulnerabilita-list')
    else:
        form = VulnerabilitaForm()
    return render(request, 'vulnerabilita/form.html', {'form': form, 'azione': 'Aggiungi'})


@login_required
@require_livello(5)
def vulnerabilita_edit(request, pk):
    vuln = get_object_or_404(Vulnerabilita, pk=pk)
    if request.method == 'POST':
        form = VulnerabilitaForm(request.POST, instance=vuln)
        if form.is_valid():
            form.save()
            messages.success(request, 'Vulnerabilità aggiornata.')
            return redirect('vulnerabilita-detail', pk=pk)
    else:
        form = VulnerabilitaForm(instance=vuln)
    return render(request, 'vulnerabilita/form.html', {'form': form, 'azione': 'Modifica'})


# ===========================================================================
# CONTROMISURE
# ===========================================================================

def contromisure_list(request):
    qs = Contromisura.objects.order_by('tipo', 'nome')
    return render(request, 'contromisure/list.html', {'contromisure': qs})


def contromisura_detail(request, pk):
    contromisura = get_object_or_404(Contromisura, pk=pk)
    mitiga_qs = Mitiga.objects.filter(
        id_contromisura=contromisura
    ).select_related('id_attacco')
    return render(request, 'contromisure/detail.html', {
        'contromisura': contromisura,
        'mitiga_qs': mitiga_qs,
    })


@login_required
@require_livello(5)
def contromisura_create(request):
    if request.method == 'POST':
        form = ContromisuraForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Contromisura aggiunta.')
            return redirect('contromisure-list')
    else:
        form = ContromisuraForm()
    return render(request, 'contromisure/form.html', {'form': form, 'azione': 'Aggiungi'})


@login_required
@require_livello(5)
def contromisura_edit(request, pk):
    contromisura = get_object_or_404(Contromisura, pk=pk)
    if request.method == 'POST':
        form = ContromisuraForm(request.POST, instance=contromisura)
        if form.is_valid():
            form.save()
            messages.success(request, 'Contromisura aggiornata.')
            return redirect('contromisura-detail', pk=pk)
    else:
        form = ContromisuraForm(instance=contromisura)
    return render(request, 'contromisure/form.html', {'form': form, 'azione': 'Modifica'})


# ===========================================================================
# CASI REALI
# ===========================================================================

def casi_list(request):
    qs = CasoReale.objects.select_related('id_attacco').order_by('-anno')
    paginator = Paginator(qs, 12)
    page = paginator.get_page(request.GET.get('page'))
    return render(request, 'casi/list.html', {'page_obj': page})


def caso_detail(request, pk):
    caso = get_object_or_404(CasoReale.objects.select_related('id_attacco'), pk=pk)
    commenti = InterazioneCaso.objects.filter(
        id_caso=caso, interazione__tipo='commento'
    ).select_related('interazione__id_utente').order_by('-interazione__data')
    n_like = InterazioneCaso.objects.filter(
        id_caso=caso, interazione__tipo='like'
    ).count()
    return render(request, 'casi/detail.html', {
        'caso': caso,
        'commenti': commenti,
        'n_like': n_like,
    })


@login_required
@require_livello(5)
def caso_create(request):
    if request.method == 'POST':
        form = CasoRealeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Caso reale aggiunto.')
            return redirect('casi-list')
    else:
        form = CasoRealeForm()
    return render(request, 'casi/form.html', {'form': form, 'azione': 'Aggiungi'})


@login_required
@require_livello(5)
def caso_edit(request, pk):
    caso = get_object_or_404(CasoReale, pk=pk)
    if request.method == 'POST':
        form = CasoRealeForm(request.POST, instance=caso)
        if form.is_valid():
            form.save()
            messages.success(request, 'Caso reale aggiornato.')
            return redirect('caso-detail', pk=pk)
    else:
        form = CasoRealeForm(instance=caso)
    return render(request, 'casi/form.html', {'form': form, 'azione': 'Modifica'})


# ===========================================================================
# ARTICOLI
# ===========================================================================

def articoli_list(request):
    qs = Articolo.objects.select_related('id_autore').order_by('-data_pubblicazione')
    paginator = Paginator(qs, 10)
    page = paginator.get_page(request.GET.get('page'))
    return render(request, 'articoli/list.html', {'page_obj': page})


def articolo_detail(request, pk):
    articolo = get_object_or_404(
        Articolo.objects.select_related('id_autore'), pk=pk
    )
    commenti = InterazioneArticolo.objects.filter(
        id_articolo=articolo, interazione__tipo='commento'
    ).select_related('interazione__id_utente').order_by('-interazione__data')
    n_like = InterazioneArticolo.objects.filter(
        id_articolo=articolo, interazione__tipo='like'
    ).count()
    return render(request, 'articoli/detail.html', {
        'articolo': articolo,
        'commenti': commenti,
        'n_like': n_like,
    })


@login_required
@require_livello(10)
def articolo_create(request):
    if request.method == 'POST':
        form = ArticoloForm(request.POST)
        if form.is_valid():
            articolo = form.save(commit=False)
            articolo.id_autore = get_current_user(request)
            articolo.save()
            check_and_promote(get_current_user(request), 'articolo')
            messages.success(request, 'Articolo pubblicato.')
            return redirect('articolo-detail', pk=articolo.pk)
    else:
        form = ArticoloForm()
    return render(request, 'articoli/form.html', {'form': form, 'azione': 'Scrivi'})


@login_required
def articolo_edit(request, pk):
    articolo = get_object_or_404(Articolo, pk=pk)
    utente = get_current_user(request)
    if articolo.id_autore != utente and utente.livello < 20:
        return render(request, 'errors/403.html', status=403)
    if request.method == 'POST':
        form = ArticoloForm(request.POST, instance=articolo)
        if form.is_valid():
            form.save()
            messages.success(request, 'Articolo aggiornato.')
            return redirect('articolo-detail', pk=pk)
    else:
        form = ArticoloForm(instance=articolo)
    return render(request, 'articoli/form.html', {'form': form, 'azione': 'Modifica'})


@login_required
@require_POST
def articolo_delete(request, pk):
    articolo = get_object_or_404(Articolo, pk=pk)
    utente = get_current_user(request)
    if articolo.id_autore != utente and utente.livello < 20:
        return render(request, 'errors/403.html', status=403)
    articolo.delete()
    messages.success(request, 'Articolo eliminato.')
    return redirect('articoli-list')


# ===========================================================================
# UTENTI / PROFILI
# ===========================================================================

def profilo_view(request, user_id):
    utente_profilo = get_object_or_404(Utenti, pk=user_id)
    attacchi = Attacco.objects.filter(
        id_autore=utente_profilo
    ).order_by('-data_pubblicazione')[:6]
    articoli = Articolo.objects.filter(
        id_autore=utente_profilo
    ).order_by('-data_pubblicazione')[:5]
    n_follower = Seguito.objects.filter(id_utente_seguito=utente_profilo).count()
    n_seguiti = Seguito.objects.filter(id_seguace=utente_profilo).count()

    utente = get_current_user(request)
    lo_segue = False
    if utente and utente != utente_profilo:
        lo_segue = Seguito.objects.filter(
            id_seguace=utente, id_utente_seguito=utente_profilo
        ).exists()

    return render(request, 'utenti/profile.html', {
        'utente_profilo': utente_profilo,
        'attacchi': attacchi,
        'articoli': articoli,
        'n_follower': n_follower,
        'n_seguiti': n_seguiti,
        'lo_segue': lo_segue,
    })


@login_required
def profilo_edit(request):
    utente = get_current_user(request)
    if request.method == 'POST':
        form = ProfiloForm(request.POST, request.FILES, instance=utente)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profilo aggiornato.')
            return redirect('profilo', user_id=utente.pk)
    else:
        form = ProfiloForm(instance=utente)
    return render(request, 'utenti/edit.html', {'form': form})


# ===========================================================================
# SOCIAL
# ===========================================================================

@login_required
@require_POST
def follow_toggle(request, user_id):
    utente = get_current_user(request)
    target = get_object_or_404(Utenti, pk=user_id)
    if utente == target:
        messages.error(request, 'Non puoi seguire te stesso.')
        return redirect('profilo', user_id=user_id)
    seguito, created = Seguito.objects.get_or_create(
        id_seguace=utente, id_utente_seguito=target
    )
    if not created:
        seguito.delete()
        messages.info(request, f'Hai smesso di seguire {target.username}.')
    else:
        messages.success(request, f'Ora segui {target.username}.')
    return redirect('profilo', user_id=user_id)


@login_required
@require_POST
def interazione_attacco(request, pk):
    attacco = get_object_or_404(Attacco, pk=pk)
    utente = get_current_user(request)
    tipo = request.POST.get('tipo', 'like')
    testo = request.POST.get('testo_commento', '').strip()

    if tipo == 'commento' and not testo:
        messages.error(request, 'Il commento non può essere vuoto.')
        return redirect('attacco-detail', pk=pk)

    if tipo == 'like':
        existing = InterazioneAttacco.objects.filter(
            id_attacco=attacco,
            interazione__tipo='like',
            interazione__id_utente=utente,
        ).first()
        if existing:
            existing.interazione.delete()
            return redirect('attacco-detail', pk=pk)

    with transaction.atomic():
        inter = Interazione.objects.create(
            tipo=tipo,
            testo_commento=testo if tipo == 'commento' else None,
            id_utente=utente,
        )
        InterazioneAttacco.objects.create(interazione=inter, id_attacco=attacco)

    if tipo == 'commento':
        check_and_promote(utente, 'commento')
    return redirect('attacco-detail', pk=pk)


@login_required
@require_POST
def interazione_articolo(request, pk):
    articolo = get_object_or_404(Articolo, pk=pk)
    utente = get_current_user(request)
    tipo = request.POST.get('tipo', 'like')
    testo = request.POST.get('testo_commento', '').strip()

    if tipo == 'commento' and not testo:
        messages.error(request, 'Il commento non può essere vuoto.')
        return redirect('articolo-detail', pk=pk)

    if tipo == 'like':
        existing = InterazioneArticolo.objects.filter(
            id_articolo=articolo,
            interazione__tipo='like',
            interazione__id_utente=utente,
        ).first()
        if existing:
            existing.interazione.delete()
            return redirect('articolo-detail', pk=pk)

    with transaction.atomic():
        inter = Interazione.objects.create(
            tipo=tipo,
            testo_commento=testo if tipo == 'commento' else None,
            id_utente=utente,
        )
        InterazioneArticolo.objects.create(interazione=inter, id_articolo=articolo)

    if tipo == 'commento':
        check_and_promote(utente, 'commento')
    return redirect('articolo-detail', pk=pk)


@login_required
@require_POST
def interazione_caso(request, pk):
    caso = get_object_or_404(CasoReale, pk=pk)
    utente = get_current_user(request)
    tipo = request.POST.get('tipo', 'like')
    testo = request.POST.get('testo_commento', '').strip()

    if tipo == 'commento' and not testo:
        messages.error(request, 'Il commento non può essere vuoto.')
        return redirect('caso-detail', pk=pk)

    if tipo == 'like':
        existing = InterazioneCaso.objects.filter(
            id_caso=caso,
            interazione__tipo='like',
            interazione__id_utente=utente,
        ).first()
        if existing:
            existing.interazione.delete()
            return redirect('caso-detail', pk=pk)

    with transaction.atomic():
        inter = Interazione.objects.create(
            tipo=tipo,
            testo_commento=testo if tipo == 'commento' else None,
            id_utente=utente,
        )
        InterazioneCaso.objects.create(interazione=inter, id_caso=caso)

    if tipo == 'commento':
        check_and_promote(utente, 'commento')
    return redirect('caso-detail', pk=pk)


# ===========================================================================
# STATISTICHE — 10 query SQL d'esame
# ===========================================================================

def statistiche_view(request):
    with connection.cursor() as cur:

        # Q1 — Top 5 attacchi per numero di casi reali
        cur.execute("""
            SELECT a.nome, COUNT(c.id_caso) AS n_casi
            FROM attacco a
            JOIN caso_reale c ON c.id_attacco = a.id_attacco
            GROUP BY a.id_attacco, a.nome
            ORDER BY n_casi DESC
            LIMIT 5
        """)
        q1 = cur.fetchall()

        # Q2 — CVSS medio per famiglia di attacco
        cur.execute("""
            SELECT
              CASE
                WHEN ar.attacco_id IS NOT NULL THEN 'Rete'
                WHEN aw.attacco_id IS NOT NULL THEN 'Web'
                WHEN soc.attacco_id IS NOT NULL THEN 'Social'
                WHEN mal.attacco_id IS NOT NULL THEN 'Malware'
              END AS famiglia,
              ROUND(AVG(v.cvss_score), 2) AS media_cvss
            FROM attacco a
            JOIN sfrutta s ON s.id_attacco = a.id_attacco
            JOIN vulnerabilita v ON v.id_vulnerabilita = s.id_vulnerabilita
            LEFT JOIN attacco_rete ar ON ar.attacco_id = a.id_attacco
            LEFT JOIN attacco_web aw ON aw.attacco_id = a.id_attacco
            LEFT JOIN attacco_social soc ON soc.attacco_id = a.id_attacco
            LEFT JOIN attacco_malware mal ON mal.attacco_id = a.id_attacco
            GROUP BY famiglia
        """)
        q2 = cur.fetchall()

        # Q3 — Contromisure che mitigano >= 3 famiglie diverse
        cur.execute("""
            SELECT c.nome, COUNT(DISTINCT famiglia) AS famiglie_coperte
            FROM contromisura c
            JOIN mitiga m ON m.id_contromisura = c.id_contromisura
            JOIN (
              SELECT attacco_id, 'rete' AS famiglia FROM attacco_rete
              UNION ALL SELECT attacco_id, 'web' FROM attacco_web
              UNION ALL SELECT attacco_id, 'social' FROM attacco_social
              UNION ALL SELECT attacco_id, 'malware' FROM attacco_malware
            ) f ON f.attacco_id = m.id_attacco
            GROUP BY c.id_contromisura, c.nome
            HAVING COUNT(DISTINCT famiglia) >= 3
        """)
        q3 = cur.fetchall()

        # Q4 — Utenti livello >= 10 ordinati per numero di articoli
        cur.execute("""
            SELECT u.username, u.livello, COUNT(a.id_articolo) AS n_articoli
            FROM utenti u
            LEFT JOIN articolo a ON a.id_autore = u.id_utente
            WHERE u.livello >= 10
            GROUP BY u.id_utente, u.username, u.livello
            ORDER BY n_articoli DESC
        """)
        q4 = cur.fetchall()

        # Q5 — Attacchi Web OWASP A03 mai commentati
        cur.execute("""
            SELECT a.nome
            FROM attacco a
            JOIN attacco_web aw ON aw.attacco_id = a.id_attacco
            WHERE aw.owasp_category = 'A03'
              AND NOT EXISTS (
                SELECT 1 FROM interazione_attacco ia
                JOIN interazione i ON i.id_interazione = ia.interazione_id
                WHERE ia.id_attacco = a.id_attacco AND i.tipo = 'commento'
              )
        """)
        q5 = cur.fetchall()

        # Q6 — Utenti seguiti da >= 5 persone
        cur.execute("""
            SELECT u.username, COUNT(s.id_seguace) AS n_follower
            FROM utenti u
            JOIN seguito s ON s.id_utente_seguito = u.id_utente
            GROUP BY u.id_utente, u.username
            HAVING COUNT(s.id_seguace) >= 5
            ORDER BY n_follower DESC
        """)
        q6 = cur.fetchall()

        # Q7 — Danno totale per anno (solo casi > 100M USD)
        cur.execute("""
            SELECT anno, SUM(danno_stimato_usd) AS danno_annuo
            FROM caso_reale
            WHERE danno_stimato_usd > 100000000
            GROUP BY anno
            ORDER BY anno DESC
        """)
        q7 = cur.fetchall()

        # Q8 — Vulnerabilità recenti (>= 2023) senza contromisure
        cur.execute("""
            SELECT v.codice_cve, v.descrizione, v.cvss_score
            FROM vulnerabilita v
            WHERE v.anno_scoperta >= 2023
              AND NOT EXISTS (
                SELECT 1 FROM sfrutta s
                JOIN mitiga m ON m.id_attacco = s.id_attacco
                WHERE s.id_vulnerabilita = v.id_vulnerabilita
              )
        """)
        q8 = cur.fetchall()

        # Q9 — Tutte le interazioni dell'utente loggato (UNION delle 3 sottoclassi)
        utente = get_current_user(request)
        uid = utente.pk if utente else 0
        cur.execute("""
            SELECT 'attacco' AS target, ia.id_attacco AS id_target, i.data, i.tipo
            FROM interazione i JOIN interazione_attacco ia ON ia.interazione_id = i.id_interazione
            WHERE i.id_utente = %s
            UNION ALL
            SELECT 'articolo', iart.id_articolo, i.data, i.tipo
            FROM interazione i JOIN interazione_articolo iart ON iart.interazione_id = i.id_interazione
            WHERE i.id_utente = %s
            UNION ALL
            SELECT 'caso', ic.id_caso, i.data, i.tipo
            FROM interazione i JOIN interazione_caso ic ON ic.interazione_id = i.id_interazione
            WHERE i.id_utente = %s
            ORDER BY data DESC
        """, [uid, uid, uid])
        q9 = cur.fetchall()

        # Q10 — Attacco più pericoloso per vittima (subquery correlata)
        cur.execute("""
            SELECT c.vittima, a.nome, c.danno_stimato_usd
            FROM caso_reale c
            JOIN attacco a ON a.id_attacco = c.id_attacco
            WHERE c.danno_stimato_usd = (
              SELECT MAX(c2.danno_stimato_usd)
              FROM caso_reale c2 WHERE c2.vittima = c.vittima
            )
            ORDER BY c.danno_stimato_usd DESC
        """)
        q10 = cur.fetchall()

    return render(request, 'statistiche.html', {
        'q1': q1, 'q2': q2, 'q3': q3, 'q4': q4, 'q5': q5,
        'q6': q6, 'q7': q7, 'q8': q8, 'q9': q9, 'q10': q10,
    })
