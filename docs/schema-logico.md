# Schema logico relazionale

Traduzione del modello ER (@er-model.md) in schema relazionale.
Strategia di traduzione della generalizzazione: **una tabella per classe**
(superclasse + N tabelle sottoclasse), pattern usato anche in MySpider.

## Tabelle

### utenti
```
utenti(id_utente PK, username UQ, email UQ, password, data_registrazione,
       livello, bio)
```

### attacco (superclasse)
```
attacco(id_attacco PK, nome, descrizione, severita, data_pubblicazione,
        riferimento_mitre, id_autore FK→utenti)
```

### Sottoclassi di attacco
```
attacco_rete(id_attacco PK/FK→attacco, protocollo, porta_bersaglio, livello_osi)
attacco_web(id_attacco PK/FK→attacco, tipo_injection, owasp_category, url_esempio)
attacco_social(id_attacco PK/FK→attacco, canale, leva_psicologica)
attacco_malware(id_attacco PK/FK→attacco, tipo_payload, persistenza, propagazione)
```

### vulnerabilita
```
vulnerabilita(id_vulnerabilita PK, codice_cve UQ, descrizione, cvss_score,
              software_affetto, anno_scoperta)
```

### contromisura
```
contromisura(id_contromisura PK, nome, descrizione, tipo)
```

### caso_reale
```
caso_reale(id_caso PK, nome_incidente, anno, vittima, danno_stimato_usd,
           descrizione_breve, id_attacco FK→attacco)
```

### articolo
```
articolo(id_articolo PK, titolo, testo, data_pubblicazione,
         id_autore FK→utenti)
```

### interazione (superclasse)
```
interazione(id_interazione PK, tipo, testo_commento NULL, data,
            id_utente FK→utenti)
```

### Sottoclassi di interazione
```
interazione_attacco(id_interazione PK/FK→interazione, id_attacco FK→attacco)
interazione_articolo(id_interazione PK/FK→interazione, id_articolo FK→articolo)
interazione_caso(id_interazione PK/FK→interazione, id_caso FK→caso_reale)
```

### Relazioni M:N
```
sfrutta(id_attacco FK, id_vulnerabilita FK, PK composta)
mitiga(id_contromisura FK, id_attacco FK, efficacia, PK composta)
seguito(id_seguito PK, id_seguace FK→utenti, id_utente_seguito FK→utenti,
        CHECK id_seguace ≠ id_utente_seguito,
        UQ(id_seguace, id_utente_seguito))
```

## Vincoli di integrità

- Tutte le FK: `ON DELETE CASCADE` per sottoclassi, `ON DELETE RESTRICT` per FK
  verso utenti (non si eliminano utenti con contenuti pubblicati).
- `severita` ∈ enum via CHECK constraint.
- `cvss_score` BETWEEN 0 AND 10.
- `anno_scoperta` ≥ 1980 AND ≤ YEAR(CURRENT_DATE).

## Conteggio

- **Tabelle totali:** 15 (8 entità principali + 4 sottoclassi attacco +
  3 sottoclassi interazione)
- **Generalizzazioni:** 2
- **Relazioni M:N:** 3

## File correlati

- Modello ER → @er-model.md
- Query SQL → @query-esame.md
- DDL completo → `docs/sql/create_tables.sql` *(da generare)*
