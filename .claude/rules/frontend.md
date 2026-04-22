# Regole frontend

## Stack

- **Django Templates** (no Jinja2, no SPA)
- **Bootstrap 5.3** via CDN (come MySpider)
- **JS vanilla** per interattività base (no React/Vue)
- Icone: **Bootstrap Icons** (`bi-*`)

## Template base

Un unico `templates/base.html` con blocchi estendibili:
```django
{% block title %}CyberPedia{% endblock %}
{% block content %}{% endblock %}
{% block extra_js %}{% endblock %}
```

Tutte le altre pagine ereditano con `{% extends 'base.html' %}`.

## Organizzazione template

```
templates/
├── base.html
├── partials/           # componenti riutilizzabili
│   ├── navbar.html
│   ├── footer.html
│   ├── card_attacco.html
│   └── form_errors.html
├── auth/
│   ├── login.html
│   └── register.html
├── attacchi/
│   ├── list.html
│   ├── detail.html
│   └── form.html
├── articoli/
└── utenti/
    └── profile.html
```

## Color palette

Tema scuro cybersecurity (non deciso nel PDF MySpider — qui abbiamo libertà):
- Sfondo: `#0d1117` (GitHub dark)
- Testo: `#e6edf3`
- Accento primario: `#f85149` (rosso "alert")
- Accento secondario: `#58a6ff` (blu link)
- Successo: `#3fb950`

Se il prof preferisce tema chiaro, cambiare in `static/css/theme.css`.

## Componenti ricorrenti

### Card attacco
```html
<div class="card bg-dark border-danger">
  <div class="card-header">
    <span class="badge bg-{{ attacco.severita_class }}">
      {{ attacco.severita }}
    </span>
    {{ attacco.nome }}
  </div>
  <div class="card-body">
    <p>{{ attacco.descrizione|truncatewords:30 }}</p>
  </div>
</div>
```

### Form Django
Usare sempre `{{ form.as_p }}` **evitato** — preferire rendering manuale con
classi Bootstrap:
```html
<div class="mb-3">
  <label class="form-label">{{ form.nome.label }}</label>
  {{ form.nome|add_class:"form-control" }}
  {% if form.nome.errors %}
    <div class="invalid-feedback d-block">{{ form.nome.errors.0 }}</div>
  {% endif %}
</div>
```

Richiede `django-widget-tweaks` in `requirements.txt`.

## Accessibilità minima

- Tutti i `<form>` hanno `<label for="">`
- Tutte le `<img>` hanno `alt=""`
- Contrast ratio ≥ 4.5:1 per testo normale
- Focus state visibile su tutti gli elementi interattivi

## Mobile

Bootstrap 5 è mobile-first. Testare a 375px di larghezza minima.
Navbar deve collassare in hamburger sotto 768px.

## File correlati

- Architettura → @../../docs/architecture.md
- CLAUDE.md → @../../CLAUDE.md
