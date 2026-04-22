# Convenzioni Django per CyberPedia

## Naming

- **Modelli Python:** PascalCase singolare inglese → `class Attacco`, `class Utenti`
  - Eccezione: `Utenti` (plurale) per coerenza con MySpider
- **Nomi tabelle DB:** snake_case, italiano, come MySpider
  - Override via `class Meta: db_table = 'attacco'`
- **Campi:** snake_case italiano → `data_pubblicazione`, `id_autore`
- **View functions:** snake_case inglese → `def attack_detail(request, pk):`
- **URL names:** kebab-case → `attack-detail`, `user-profile`
- **Template:** kebab-case → `attack-detail.html`

## Pattern per generalizzazioni

**Modello superclasse:**
```python
class Attacco(models.Model):
    nome = models.CharField(max_length=200)
    # ... campi comuni
    class Meta:
        db_table = 'attacco'
```

**Modello sottoclasse (pattern "tabella per classe"):**
```python
class AttaccoWeb(models.Model):
    attacco = models.OneToOneField(
        Attacco, on_delete=models.CASCADE,
        primary_key=True, related_name='web'
    )
    tipo_injection = models.CharField(max_length=50)
    # ...
    class Meta:
        db_table = 'attacco_web'
```

⚠️ **Non usare** `class Meta: abstract = True` né `multi_table_inheritance`:
vogliamo il controllo esplicito sulla struttura, come in MySpider.

## Views

- **Preferire function-based views** (come MySpider). Class-based views
  solo se strettamente necessario (es. `LoginView`).
- Ogni view inizia con:
  ```python
  def my_view(request, ...):
      if not request.session.get('user_id'):
          return redirect('login')
      user = Utenti.objects.get(id=request.session['user_id'])
  ```
- Usare `@require_POST` / `@require_GET` dove appropriato.

## Forms

- `ModelForm` ove possibile, `Form` custom per logica complessa
  (es. registrazione con 3 campi password/conferma).
- Validazione password nel form, non nella view.

## ORM — Anti-pattern da evitare

- ❌ N+1 queries → usare `.select_related()` per FK, `.prefetch_related()` per M:N
- ❌ `Attacco.objects.all()` in template (usa view)
- ❌ Query raw SQL senza motivazione (ma per l'orale **una o due query raw**
  nelle view statistiche sono utili per dimostrare conoscenza SQL)

## Struttura views.py

Organizzare in sezioni commentate:
```python
# ===== AUTH =====
def register(request): ...
def login(request): ...

# ===== ATTACCHI =====
def attack_list(request): ...
def attack_detail(request, pk): ...

# ===== SOCIAL =====
def follow_user(request, user_id): ...
```

## File correlati

- CLAUDE.md → @../../CLAUDE.md
- Database → @database.md
- Sicurezza → @security.md
