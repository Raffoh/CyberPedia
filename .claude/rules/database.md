# Regole database e migrazioni

## Nomi tabelle

**Sempre** override esplicito del nome tabella:
```python
class Meta:
    db_table = 'nome_tabella_italiano'
```

Motivo: Django di default aggiunge prefisso app (`core_attacco`), noi vogliamo
nomi puliti come MySpider (`attacco`).

## Migrazioni

- ✅ Committare **tutti** i file `migrations/*.py`
- ✅ Un file migrazione per cambiamento logico (non accumulare)
- ❌ **MAI** cancellare migrazioni già applicate in produzione
- ❌ **MAI** `python manage.py migrate --fake` senza discutere

Se bisogna resettare in locale:
```bash
rm -rf core/migrations/0*.py
rm db.sqlite3
python manage.py makemigrations core
python manage.py migrate
python manage.py loaddata fixtures/seed.json
```

## Vincoli di integrità

Dove possibile, esprimerli nel modello:
```python
from django.db.models import CheckConstraint, Q

class Vulnerabilita(models.Model):
    cvss_score = models.DecimalField(max_digits=3, decimal_places=1)
    class Meta:
        db_table = 'vulnerabilita'
        constraints = [
            CheckConstraint(
                check=Q(cvss_score__gte=0) & Q(cvss_score__lte=10),
                name='cvss_range'
            )
        ]
```

## Foreign Keys: regole di cancellazione

- `id_autore` su Articolo/Attacco → `PROTECT` (non eliminare utenti autori)
- Sottoclassi → `CASCADE` (eliminare Attacco elimina AttaccoWeb, ecc.)
- Interazioni → `CASCADE` (eliminare articolo/attacco elimina interazioni)
- Seguito → `CASCADE` (se un utente si cancella, spariscono i suoi follow)

## Indici

Aggiungere `db_index=True` su:
- Tutte le FK (Django lo fa di default, ma verificare)
- Campi usati frequentemente in `WHERE` (es. `codice_cve`, `anno_scoperta`)
- Campi usati in `ORDER BY` frequenti

## Fixtures

Mantenere `fixtures/seed.json` con dati demo minimi ma significativi:
- 5-8 utenti (livelli diversi)
- 15-20 attacchi (distribuiti sulle 4 sottoclassi)
- 10 vulnerabilità (CVE reali)
- 8 contromisure
- 15 casi reali famosi
- 5 articoli
- Interazioni sparse

## Dump per consegna

```bash
# SQL dump (richiesto all'esame)
sqlite3 db.sqlite3 .dump > dump.sql

# JSON fixture (utile per re-popolare)
python manage.py dumpdata --indent 2 core > fixtures/seed.json
```

## File correlati

- Schema logico → @../../docs/schema-logico.md
- Django conventions → @django-conventions.md
