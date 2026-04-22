# Sicurezza e autenticazione

## Pattern generale (ereditato da MySpider)

Autenticazione **custom**, separata da `django.contrib.auth`:
- Tabella `utenti` contiene password, non `auth_user`
- Login basato su sessioni Django (`request.session`)
- Hashing password con `pbkdf2_sha256` (funzioni `make_password` / `check_password`
  da `django.contrib.auth.hashers`)

## Registrazione

Validazione password:
- Lunghezza ≥ 8 caratteri
- Almeno 1 numero (`[0-9]`)
- Almeno 1 simbolo speciale (`[!@#$%^&*...]`)
- Almeno 1 lettera maiuscola (opzionale ma consigliato)

Email unica e validata con `EmailValidator` Django.
Username unico, lunghezza 3-20, regex `^[a-zA-Z0-9_]+$`.

## Login: blocco per tentativi falliti

Pattern MySpider:
- 3 tentativi falliti consecutivi → blocco 15 minuti
- Contatore tentativi e timestamp salvati in sessione:
  ```python
  request.session['login_attempts'] = 0
  request.session['lockout_until'] = None
  ```
- Dopo login riuscito, reset contatore

## Livelli utente e autorizzazione

Il campo `livello` (int) determina privilegi:

| Livello | Privilegio |
|---|---|
| 0-4 | Utente base: può leggere, commentare, seguire |
| 5-9 | Contributor: può creare Vulnerabilità, Contromisure, CasoReale |
| 10-19 | Esperto: può creare Attacchi e Articoli |
| 20+ | Admin: può moderare, modificare contenuti altrui |

Decorator custom:
```python
def require_livello(min_level):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            user = get_current_user(request)
            if not user or user.livello < min_level:
                return render(request, 'errors/403.html', status=403)
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator
```

Uso:
```python
@require_livello(10)
def create_attack(request): ...
```

## Promozione automatica livello

Quando un utente supera soglie di contributi, livello incrementato:
- +1 livello ogni 3 commenti utili
- +1 livello per ogni articolo pubblicato
- +2 livelli per ogni attacco validato (se ci sarà validazione)

Logica in `core/services/leveling.py` (da creare).

## Protezione CSRF

Django lo fa di default. **Non disabilitare** `CsrfViewMiddleware`.
Tutti i form POST devono includere `{% csrf_token %}`.

## SQL Injection

Siamo su Django ORM → safe by default.
Se si usa `raw()` o `cursor.execute()`:
- ✅ `Attacco.objects.raw('SELECT * FROM attacco WHERE id = %s', [pk])`
- ❌ `f"SELECT * FROM attacco WHERE id = {pk}"`

## XSS

Django escape di default in template. Non usare `|safe` senza necessità
estrema e solo su contenuti validati (non input utente diretti).

## File upload

Campo `ImageField` con validazione:
- Tipo MIME consentito: image/jpeg, image/png, image/webp, image/gif
- Dimensione max: 5 MB
- Validazione con Pillow che sia un'immagine reale (non solo estensione)

## Secret management

- `SECRET_KEY` Django → in `.env`, non in `settings.py`
- `.env` in `.gitignore`
- Fornire `.env.example` con placeholder per clonazione

## File correlati

- Django conventions → @django-conventions.md
- CLAUDE.md → @../../CLAUDE.md
