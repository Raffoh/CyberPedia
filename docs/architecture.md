# Architettura del progetto

## Struttura directory

```
cyberpedia/
├── CLAUDE.md                    # Memoria principale Claude Code
├── manage.py
├── requirements.txt
├── db.sqlite3                   # DB locale (non in git)
├── dump.sql                     # Dump DB per consegna esame
├── README.md                    # Doc per utente finale
│
├── cyberpedia/                  # Config Django
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── core/                        # App principale (unica, pattern MySpider)
│   ├── models.py                # Tutti i modelli del dominio
│   ├── views.py                 # View-based views (no CBV per semplicità esame)
│   ├── urls.py
│   ├── forms.py
│   ├── admin.py
│   ├── migrations/
│   └── templatetags/
│
├── templates/                   # Template globali
│   ├── base.html
│   ├── auth/
│   ├── attacchi/
│   ├── articoli/
│   └── utenti/
│
├── static/                      # CSS, JS, immagini statiche
│   ├── css/
│   ├── js/
│   └── img/
│
├── media/                       # Upload utente (foto profilo, icone)
│   └── attacchi_img/
│
├── docs/                        # Documentazione progettuale
│   ├── er-model.md
│   ├── schema-logico.md
│   ├── query-esame.md
│   ├── architecture.md          # questo file
│   ├── myspider-reference.md
│   ├── roadmap.md
│   ├── er-diagram.png           # immagine ER
│   └── sql/
│       └── create_tables.sql
│
└── .claude/
    └── rules/
        ├── django-conventions.md
        ├── database.md
        ├── frontend.md
        ├── security.md
        └── git-workflow.md
```

## Scelte architetturali chiave

### Singola app Django (`core`)
Come MySpider usa una sola app `My_Spider`, anche CyberPedia concentra tutti
i modelli in un'app unica. Motivo: **il progetto è centrato sullo schema DB**,
non sulla modularità applicativa.

### Modello utente custom separato da `auth_user`
La tabella `utenti` è indipendente da `django.contrib.auth.User` per rispecchiare
esattamente il pattern MySpider. L'autenticazione viene gestita con sessioni
custom + hashing password (`pbkdf2_sha256`). Vedi @.claude/rules/security.md.

### Traduzione della generalizzazione: "tabella per classe"
Superclasse + tabella separata per ogni sottoclasse. Alternativa scartata:
"tabella unica" (spreco di NULL) e "solo sottoclassi" (perde polimorfismo).

### Template globali, non per-app
I template stanno in `/templates/`, non dentro `core/templates/core/`, per
mantenere il pattern MySpider (i template del progetto originale sono globali).

## Flusso di una richiesta tipo

1. Utente → URL → `cyberpedia/urls.py` → `core/urls.py`
2. View in `core/views.py` verifica autenticazione (decorator custom)
3. View interroga i modelli (`core/models.py`)
4. View renderizza template da `/templates/`
5. Template estende `base.html` e usa Bootstrap 5

## File correlati

- Convenzioni Django → @../.claude/rules/django-conventions.md
- Schema DB → @schema-logico.md
