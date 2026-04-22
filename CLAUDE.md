# CyberPedia

> Piattaforma gestionale e social per la knowledge base di attacchi informatici.
> Progetto d'esame per il corso **Basi di Dati** — ispirato allo stile di
> [MySpider](https://github.com/MagicDog01/My_Spider).

---

## 🎯 WHY — Obiettivo del progetto

CyberPedia è un'applicazione web che consente a studenti e professionisti della
sicurezza informatica di **consultare, documentare e commentare** attacchi
informatici reali. È un progetto universitario focalizzato sulla **modellazione
relazionale**: deve dimostrare padronanza di ER, generalizzazioni, normalizzazione
e SQL avanzato. La componente applicativa (Django) è **al servizio** del database,
non viceversa.

## 🧱 WHAT — Stack e struttura

- **Backend:** Python 3.10+ · Django 5.x · Pillow
- **Database:** SQLite (in dev) con schema esportabile in `dump.sql`
- **Frontend:** HTML5 · CSS3 · Bootstrap 5 · Django Templates
- **Auth:** custom (no `django.contrib.auth.User` per le entità utente di dominio)

Mappa della codebase: @docs/architecture.md

## 🗺️ HOW — Come lavorare su questo progetto

Prima di scrivere codice, Claude deve **sempre** consultare il file rilevante
tra quelli linkati qui sotto. Non duplicare informazioni: se serve un
dettaglio, segui il link.

### Documentazione di dominio (sempre rilevante)
- Modello ER e generalizzazioni → @docs/er-model.md
- Schema logico relazionale → @docs/schema-logico.md
- Query SQL "da esame" richieste → @docs/query-esame.md

### Regole di sviluppo (caricate su richiesta)
- Convenzioni Django e naming → @.claude/rules/django-conventions.md
- Regole database e migrazioni → @.claude/rules/database.md
- Stile frontend (template/Bootstrap) → @.claude/rules/frontend.md
- Sicurezza e autenticazione → @.claude/rules/security.md
- Workflow Git e commit → @.claude/rules/git-workflow.md

## ⚡ Comandi essenziali

```bash
# Setup iniziale (solo la prima volta)
python -m venv venv && source venv/bin/activate  # Linux/Mac
# .\venv\Scripts\activate                         # Windows
pip install -r requirements.txt

# Database
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser

# Sviluppo
python manage.py runserver        # http://127.0.0.1:8000/

# Dump/restore DB (richiesto dal prof)
python manage.py dumpdata > fixtures/seed.json
sqlite3 db.sqlite3 .dump > dump.sql
```

## 🚨 Gotchas — Cose che DEVI sapere

1. **Due generalizzazioni ER**: `Attacco` (4 sottoclassi per vettore) e
   `Interazione` (3 sottoclassi per target). Ogni modifica allo schema va
   riflessa in **entrambe** le sottoclassi e nella documentazione ER. Dettagli
   in @docs/er-model.md.
2. **Utente custom**: il modello `Utenti` è separato da `auth_user` (pattern
   MySpider). Non sostituirlo con `AbstractUser` senza discutere prima.
3. **Livelli utente**: il campo `livello` (intero) **non è un ruolo Django**,
   è un attributo di dominio che abilita privilegi (pubblicare attacchi,
   scrivere articoli). Vedi @.claude/rules/security.md.
4. **Naming italiano**: tabelle ed entità in italiano (come MySpider):
   `utenti`, `attacco`, `articolo`. Codice Python in inglese.
5. **No auto-migrate in produzione**: le migrazioni vanno committate
   esplicitamente, mai rigenerate da zero.
6. **Documentazione d'esame**: ogni modifica allo schema richiede aggiornamento
   del diagramma ER (`docs/er-diagram.png`) e del PDF finale.

## 📋 Stato del progetto

- [ ] Progettazione ER completata
- [ ] Schema logico tradotto
- [ ] Modelli Django creati
- [ ] Migrazioni applicate
- [ ] CRUD base funzionante
- [ ] Autenticazione custom
- [ ] Sistema social (follow + interazioni)
- [ ] Articoli con sistema livelli
- [ ] Query SQL d'esame testate
- [ ] Frontend con Bootstrap
- [ ] Documentazione PDF

Tracking dettagliato: @docs/roadmap.md

---

**Ricorda:** quando in dubbio sulla modellazione, **MySpider è lo standard di
riferimento stilistico**. Schema analizzato in @docs/myspider-reference.md.
