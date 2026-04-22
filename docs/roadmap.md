# Roadmap di sviluppo

Ordine di implementazione suggerito. Non procedere a un blocco se il
precedente non è completo e testato.

## Fase 1 — Progettazione concettuale ⚙️
- [ ] Diagramma ER disegnato (strumento: dbdiagram.io / draw.io / ERDPlus)
- [ ] Diagramma ER con generalizzazioni risolte
- [ ] Schema logico tradotto (ved. @schema-logico.md)
- [ ] DDL SQL completo in `docs/sql/create_tables.sql`
- [ ] Diagramma ER esportato come `docs/er-diagram.png`

## Fase 2 — Setup Django 🛠️
- [ ] `django-admin startproject cyberpedia`
- [ ] `python manage.py startapp core`
- [ ] Configurare `settings.py`: italiano, timezone Europe/Rome, MEDIA_URL
- [ ] Aggiungere `core` a INSTALLED_APPS
- [ ] Creare `requirements.txt`

## Fase 3 — Modelli e DB 🗃️
- [ ] Modello `Utenti` (custom, non AbstractUser)
- [ ] Modello `Attacco` + 4 sottoclassi (OneToOneField verso Attacco)
- [ ] Modello `Vulnerabilita`, `Contromisura`, `CasoReale`
- [ ] Modello `Articolo`
- [ ] Modello `Interazione` + 3 sottoclassi
- [ ] Modello `Seguito` con vincolo auto-riferimento
- [ ] Tabelle M:N: `Sfrutta`, `Mitiga`
- [ ] `makemigrations` + `migrate`
- [ ] Fixture iniziali (`fixtures/seed.json`)

## Fase 4 — Auth e utenti 🔐
- [ ] Form registrazione con validazione password (≥8 char, 1 num, 1 simbolo)
- [ ] Form login + logica blocco dopo 3 tentativi (15 min)
- [ ] Middleware/decorator `@login_required` custom
- [ ] Pagina profilo utente
- [ ] Sistema livelli: promozione automatica dopo N contributi

## Fase 5 — Funzionalità core 📚
- [ ] CRUD Attacco (con form polimorfico per sottoclasse)
- [ ] CRUD Vulnerabilità e Contromisure (solo livello ≥ X)
- [ ] CRUD CasoReale
- [ ] CRUD Articolo (solo livello ≥ X)
- [ ] Dettaglio attacco con vulnerabilità/contromisure collegate
- [ ] Upload immagini (Pillow)

## Fase 6 — Funzionalità social 👥
- [ ] Like/commento su Attacco, Articolo, CasoReale
- [ ] Follow/unfollow utenti
- [ ] Feed con attività degli utenti seguiti
- [ ] Notifiche (opzionale)

## Fase 7 — Query SQL e reportistica 📊
- [ ] Implementare le 10 query di @query-esame.md come view statistiche
- [ ] Pagina "Statistiche" con grafici (Chart.js opzionale)
- [ ] Export CSV (opzionale)

## Fase 8 — Polish 🎨
- [ ] Template base con Bootstrap 5
- [ ] Navbar, footer, pagine errore 404/500
- [ ] Logo e branding
- [ ] Responsive check mobile

## Fase 9 — Documentazione consegna 📄
- [ ] Documento PDF con: introduzione, ER, schema logico, query, screenshot
- [ ] README aggiornato con credenziali demo
- [ ] Dump SQL finale
- [ ] Rimozione dati sensibili dal repo

## File correlati

- CLAUDE.md principale → @../CLAUDE.md
- Stato corrente → controllare checkbox sopra
