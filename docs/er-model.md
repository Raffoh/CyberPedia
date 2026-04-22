# Modello Entity-Relationship

## Entità principali

### UTENTE
Attributi: `id_utente` (PK), `username` (UQ, max 20), `email` (UQ), `password`
(hash), `data_registrazione`, `livello` (int), `bio` (opz).

### ATTACCO *(superclasse)*
Attributi: `id_attacco` (PK), `nome`, `descrizione`, `severità` ∈
{bassa, media, alta, critica}, `data_pubblicazione`, `riferimento_mitre` (opz),
`id_autore` (FK → Utente).

### ⚡ Generalizzazione su ATTACCO (totale, esclusiva)

| Sottoclasse | Attributi specifici |
|---|---|
| **AttaccoRete** | `protocollo`, `porta_bersaglio`, `livello_OSI` |
| **AttaccoWeb** | `tipo_injection`, `owasp_category`, `url_vulnerabile_esempio` |
| **AttaccoSocial** | `canale` (email/SMS/tel/social), `leva_psicologica` |
| **AttaccoMalware** | `tipo_payload`, `persistenza` (bool), `propagazione` |

**Vincolo di copertura:** ogni Attacco appartiene a esattamente una sottoclasse.

### VULNERABILITÀ
`id_vulnerabilita` (PK), `codice_CVE`, `descrizione`, `cvss_score`,
`software_affetto`, `anno_scoperta`.

### CONTROMISURA
`id_contromisura` (PK), `nome`, `descrizione`, `tipo` ∈
{preventiva, rilevativa, correttiva}.

### CASO_REALE *(eventi storici)*
`id_caso` (PK), `nome_incidente`, `anno`, `vittima`, `danno_stimato_usd`,
`descrizione_breve`, `id_attacco` (FK → Attacco).

### ARTICOLO
`id_articolo` (PK), `titolo`, `testo`, `data_pubblicazione`,
`id_autore` (FK → Utente).

### INTERAZIONE *(superclasse)*
`id_interazione` (PK), `tipo` ∈ {like, commento, segnalazione},
`testo_commento` (nullable), `data`, `id_utente` (FK).

### ⚡ Generalizzazione su INTERAZIONE (totale, esclusiva)

| Sottoclasse | FK specifica |
|---|---|
| **InterazioneAttacco** | `id_attacco` |
| **InterazioneArticolo** | `id_articolo` |
| **InterazioneCaso** | `id_caso` |

### SEGUITO
`id_seguito` (PK), `id_seguace` (FK → Utente), `id_seguito` (FK → Utente).
Vincolo: `id_seguace ≠ id_seguito`.

---

## Relazioni M:N

| Nome | Entità | Attributi relazione |
|---|---|---|
| **SFRUTTA** | Attacco ↔ Vulnerabilità | — |
| **MITIGA** | Contromisura ↔ Attacco | `efficacia` ∈ {bassa, media, alta} |

## Cardinalità riassuntive

- Utente 1 : N Attacco (un utente esperto pubblica più attacchi)
- Utente 1 : N Articolo
- Attacco 1 : N CasoReale
- Attacco M : N Vulnerabilità (via SFRUTTA)
- Attacco M : N Contromisura (via MITIGA)
- Utente M : N Utente (via SEGUITO, auto-relazione)
- Utente 1 : N Interazione
- Interazione 1 : 1 {Attacco | Articolo | Caso} (via generalizzazione)

## File correlati

- Traduzione in schema logico → @schema-logico.md
- Diagramma ER grafico → `docs/er-diagram.png` *(da generare)*
- Confronto con MySpider → @myspider-reference.md
