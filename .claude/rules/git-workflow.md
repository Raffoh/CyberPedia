# Git workflow

## Branch strategy

Progetto solo (no team) → workflow semplificato:
- `master` (o `main`): branch stabile, pronto per consegna
- `dev`: branch di sviluppo
- `feature/<nome>`: branch per feature singola, mergiata in `dev`

## Commit message convention

Formato: `<tipo>: <descrizione breve>`

Tipi:
- `feat`: nuova funzionalità
- `fix`: bugfix
- `db`: modifiche a modelli/migrazioni
- `doc`: documentazione
- `style`: CSS/template, nessuna logica
- `refactor`: refactoring senza cambio comportamento
- `chore`: config, dipendenze, setup

Esempi:
- `feat: aggiunto CRUD per Vulnerabilità`
- `db: creata generalizzazione Interazione + 3 sottoclassi`
- `fix: validazione password registrazione non funzionava`
- `doc: aggiornata documentazione ER con cardinalità`

## Cosa NON committare

Già in `.gitignore`:
- `venv/`, `__pycache__/`, `*.pyc`
- `db.sqlite3` (eccetto se richiesto per consegna)
- `media/` (file upload utente)
- `.env`
- `.idea/`, `.vscode/settings.json`
- `*.log`

Da committare **solo alla consegna**:
- `dump.sql` (snapshot DB con dati demo)
- `docs/er-diagram.png` (versione finale)

## Prima di ogni commit

1. `python manage.py check` — verifica config
2. `python manage.py makemigrations --dry-run` — nessuna migrazione pending
3. Test manuale: server avviato, pagina principale carica

## Commit di fine sessione

A fine ogni sessione di lavoro con Claude Code:
```bash
git add -A
git status   # review!
git commit -m "tipo: descrizione"
git push
```

## Tag per consegne

Al momento della consegna esame:
```bash
git tag -a v1.0-consegna -m "Versione consegnata per esame DD/MM/YYYY"
git push --tags
```

## File correlati

- CLAUDE.md → @../../CLAUDE.md
- Database (per regole migrazioni) → @database.md
