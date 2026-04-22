# CyberPedia

> Piattaforma gestionale e social per la knowledge base di attacchi informatici.
> Progetto d'esame per il corso **Basi di Dati** — ispirato a [My_Spider](https://github.com/MagicDog01/My_Spider).

---

## Panoramica

**CyberPedia** è un'applicazione web che consente a studenti e professionisti della sicurezza informatica di consultare, documentare e commentare attacchi informatici reali.

Il progetto è incentrato sulla **modellazione relazionale avanzata**: dimostra padronanza di diagrammi ER, generalizzazioni (due gerarchie di ereditarietà), normalizzazione e SQL avanzato tramite 10 query d'esame esposte nella sezione *Statistiche*.

---

## Tecnologie utilizzate

### Backend
- **Python 3.10+**
- **Django 5.x**
- **Pillow** — gestione immagini (profili, attacchi)
- **django-widget-tweaks** — rendering form con Bootstrap
- **python-dotenv** — gestione variabili d'ambiente

### Database
- **SQLite** (sviluppo) — schema esportato in `dump.sql`
- Schema con **15 tabelle**, **2 generalizzazioni** ER e **3 relazioni M:N**

### Frontend
- **Bootstrap 5.3** — tema dark in stile cybersecurity
- **Bootstrap Icons**
- **Django Templates** — nessun framework JS

---

## Installazione

### Prerequisiti
- Python 3.10 o superiore
- pip

### Clona e installa

```bash
git clone https://github.com/Raffoh/CyberPedia.git
cd CyberPedia

# Crea e attiva l'ambiente virtuale
python -m venv venv
source venv/bin/activate        # Linux / Mac
# .\venv\Scripts\activate       # Windows

pip install -r requirements.txt
```

### Configura le variabili d'ambiente

```bash
cp .env.example .env
# Modifica .env con la tua SECRET_KEY se necessario
```

---

## Avvio del server

### Setup database

```bash
python manage.py migrate

# Popola il database con i dati di esempio
python manage.py seed
```

### Server di sviluppo

```bash
python manage.py runserver
```

Apri il browser su **http://127.0.0.1:8000/**

---

## Funzionalità principali

- **Catalogo attacchi** con 4 famiglie (Rete, Web, Social Engineering, Malware) — prima generalizzazione ER
- **Interazioni** (like, commento, segnalazione) su attacchi, articoli e casi reali — seconda generalizzazione ER
- **Vulnerabilità** con codice CVE e CVSS score, collegate agli attacchi tramite relazione M:N `sfrutta`
- **Contromisure** (preventiva / rilevativa / correttiva), collegate agli attacchi tramite `mitiga` con campo `efficacia`
- **Casi reali** documentati con vittima, anno e danno stimato in USD
- **Articoli** redatti dagli esperti della community
- **Sistema social**: follow/unfollow tra utenti, feed personalizzato
- **Sistema livelli**: accesso progressivo alle funzionalità in base al livello dell'utente
- **Autenticazione custom**: login con sessioni Django, hash `pbkdf2_sha256`, blocco dopo 3 tentativi falliti (15 minuti)
- **Pagina Statistiche**: 10 query SQL d'esame eseguite in raw SQL (JOIN, GROUP BY, HAVING, NOT EXISTS, UNION, subquery correlate)

---

## Credenziali demo

| Username | Password | Livello | Permessi |
|---|---|---|---|
| `admin_cp` | `Admin123!` | 20 | Amministratore — accesso completo |
| `esperto` | `Admin123!` | 15 | Esperto — crea attacchi e articoli |
| `ricercatore` | `Admin123!` | 10 | Ricercatore — crea attacchi e articoli |
| `analista` | `Admin123!` | 5 | Analista — aggiunge CVE e contromisure |
| `studente` | `Admin123!` | 3 | Studente — lettura e commenti |
| `ospite` | `Admin123!` | 0 | Ospite — solo lettura |

> **Nota:** per accedere al pannello `/admin/` di Django eseguire `python manage.py createsuperuser`.

---

## Struttura del progetto

```
CyberPedia/
├── manage.py
├── requirements.txt
├── dump.sql                    # Dump SQL per la consegna d'esame
├── README.md
├── .env.example
├── cyberpedia/                 # Configurazione Django
│   ├── settings.py
│   └── urls.py
├── core/                       # Applicazione principale
│   ├── models.py               # 15 modelli — 2 generalizzazioni
│   ├── views.py                # Viste FBV + 10 query SQL d'esame
│   ├── forms.py
│   ├── urls.py
│   ├── admin.py
│   ├── decorators.py           # @login_required, @require_livello
│   ├── auth_helpers.py
│   ├── context_processors.py
│   ├── services/
│   │   └── leveling.py         # Promozione automatica livello
│   └── management/commands/
│       └── seed.py             # python manage.py seed
├── templates/                  # Template Bootstrap 5 (dark theme)
│   ├── base.html
│   ├── home.html
│   ├── statistiche.html        # 10 query SQL d'esame
│   ├── attacchi/
│   ├── articoli/
│   ├── vulnerabilita/
│   ├── contromisure/
│   ├── casi/
│   └── utenti/
├── static/
├── media/
└── fixtures/
    └── seed.json
```

---

## Schema del database

Il database implementa due **generalizzazioni totali ed esclusive**:

**1. Attacco** → AttaccoRete | AttaccoWeb | AttaccoSocial | AttaccoMalware

**2. Interazione** → InterazioneAttacco | InterazioneArticolo | InterazioneCaso

Relazioni M:N esplicite: `sfrutta` (Attacco ↔ Vulnerabilità), `mitiga` (Contromisura ↔ Attacco, con `efficacia`), `seguito` (Utente ↔ Utente, self-referential).

---

## Query SQL d'esame

Dieci query accessibili su `/statistiche/`, eseguite tramite `connection.cursor()`:

| # | Query | Tecniche |
|---|---|---|
| Q1 | Top 5 attacchi per casi reali | JOIN, GROUP BY, COUNT |
| Q2 | CVSS medio per famiglia | LEFT JOIN, AVG, CASE |
| Q3 | Contromisure su ≥ 3 famiglie | UNION, HAVING |
| Q4 | Utenti livello ≥ 10 per articoli | LEFT JOIN, WHERE |
| Q5 | Web OWASP A03 mai commentati | NOT EXISTS correlato |
| Q6 | Utenti seguiti da ≥ 5 | Self-join, HAVING |
| Q7 | Danno totale per anno > 100M | SUM, GROUP BY |
| Q8 | CVE recenti senza contromisure | NOT EXISTS, JOIN |
| Q9 | Tutte le interazioni utente | UNION delle 3 sottoclassi |
| Q10 | Attacco più pericoloso per vittima | Subquery correlata con MAX |

---

## Licenza

MIT License — vedi [LICENSE](LICENSE)
