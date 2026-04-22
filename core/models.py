from django.db import models
from django.db.models import Q, F


# ---------------------------------------------------------------------------
# Utenti (custom, separato da auth_user — pattern MySpider)
# ---------------------------------------------------------------------------

class Utenti(models.Model):
    id_utente = models.AutoField(primary_key=True)
    username = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    data_registrazione = models.DateField(auto_now_add=True)
    livello = models.IntegerField(default=0)
    bio = models.TextField(blank=True)
    foto_profilo = models.ImageField(upload_to='profili/', blank=True, null=True)

    class Meta:
        db_table = 'utenti'

    def __str__(self):
        return self.username


# ---------------------------------------------------------------------------
# Attacco — superclasse della prima generalizzazione (totale, esclusiva)
# ---------------------------------------------------------------------------

SEVERITA_CHOICES = [
    ('bassa', 'Bassa'),
    ('media', 'Media'),
    ('alta', 'Alta'),
    ('critica', 'Critica'),
]


class Attacco(models.Model):
    id_attacco = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=200)
    descrizione = models.TextField()
    severita = models.CharField(max_length=10, choices=SEVERITA_CHOICES)
    data_pubblicazione = models.DateField()
    riferimento_mitre = models.CharField(max_length=50, blank=True)
    immagine = models.ImageField(upload_to='attacchi_img/', blank=True, null=True)
    id_autore = models.ForeignKey(
        Utenti, on_delete=models.PROTECT,
        db_column='id_autore', related_name='attacchi'
    )

    class Meta:
        db_table = 'attacco'

    def __str__(self):
        return self.nome

    def get_famiglia(self):
        for attr in ('rete', 'web', 'social', 'malware'):
            if hasattr(self, attr):
                return attr
        return 'sconosciuta'


# Sottoclassi Attacco

class AttaccoRete(models.Model):
    attacco = models.OneToOneField(
        Attacco, on_delete=models.CASCADE,
        primary_key=True, related_name='rete'
    )
    protocollo = models.CharField(max_length=20)
    porta_bersaglio = models.IntegerField(null=True, blank=True)
    livello_osi = models.CharField(max_length=20)

    class Meta:
        db_table = 'attacco_rete'

    def __str__(self):
        return f'Rete: {self.attacco.nome}'


CANALE_CHOICES = [
    ('email', 'Email'),
    ('sms', 'SMS'),
    ('telefono', 'Telefono'),
    ('social', 'Social Media'),
]

OWASP_CHOICES = [(f'A0{i}', f'A0{i}') for i in range(1, 10)] + [('A10', 'A10')]


class AttaccoWeb(models.Model):
    attacco = models.OneToOneField(
        Attacco, on_delete=models.CASCADE,
        primary_key=True, related_name='web'
    )
    tipo_injection = models.CharField(max_length=50)
    owasp_category = models.CharField(max_length=10, choices=OWASP_CHOICES)
    url_esempio = models.URLField(blank=True)

    class Meta:
        db_table = 'attacco_web'

    def __str__(self):
        return f'Web: {self.attacco.nome}'


class AttaccoSocial(models.Model):
    attacco = models.OneToOneField(
        Attacco, on_delete=models.CASCADE,
        primary_key=True, related_name='social'
    )
    canale = models.CharField(max_length=20, choices=CANALE_CHOICES)
    leva_psicologica = models.CharField(max_length=100)

    class Meta:
        db_table = 'attacco_social'

    def __str__(self):
        return f'Social: {self.attacco.nome}'


class AttaccoMalware(models.Model):
    attacco = models.OneToOneField(
        Attacco, on_delete=models.CASCADE,
        primary_key=True, related_name='malware'
    )
    tipo_payload = models.CharField(max_length=50)
    persistenza = models.BooleanField(default=False)
    propagazione = models.CharField(max_length=100)

    class Meta:
        db_table = 'attacco_malware'

    def __str__(self):
        return f'Malware: {self.attacco.nome}'


# ---------------------------------------------------------------------------
# Vulnerabilita
# ---------------------------------------------------------------------------

class Vulnerabilita(models.Model):
    id_vulnerabilita = models.AutoField(primary_key=True)
    codice_cve = models.CharField(max_length=20, unique=True, db_index=True)
    descrizione = models.TextField()
    cvss_score = models.DecimalField(max_digits=3, decimal_places=1)
    software_affetto = models.CharField(max_length=200)
    anno_scoperta = models.IntegerField(db_index=True)

    class Meta:
        db_table = 'vulnerabilita'
        constraints = [
            models.CheckConstraint(
                check=Q(cvss_score__gte=0) & Q(cvss_score__lte=10),
                name='cvss_range'
            ),
            models.CheckConstraint(
                check=Q(anno_scoperta__gte=1980),
                name='anno_scoperta_min'
            ),
        ]

    def __str__(self):
        return self.codice_cve


# ---------------------------------------------------------------------------
# Contromisura
# ---------------------------------------------------------------------------

TIPO_CONTROMISURA_CHOICES = [
    ('preventiva', 'Preventiva'),
    ('rilevativa', 'Rilevativa'),
    ('correttiva', 'Correttiva'),
]


class Contromisura(models.Model):
    id_contromisura = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=200)
    descrizione = models.TextField()
    tipo = models.CharField(max_length=12, choices=TIPO_CONTROMISURA_CHOICES)

    class Meta:
        db_table = 'contromisura'

    def __str__(self):
        return self.nome


# ---------------------------------------------------------------------------
# CasoReale
# ---------------------------------------------------------------------------

class CasoReale(models.Model):
    id_caso = models.AutoField(primary_key=True)
    nome_incidente = models.CharField(max_length=200)
    anno = models.IntegerField()
    vittima = models.CharField(max_length=200)
    danno_stimato_usd = models.BigIntegerField(null=True, blank=True)
    descrizione_breve = models.TextField()
    id_attacco = models.ForeignKey(
        Attacco, on_delete=models.PROTECT,
        db_column='id_attacco', related_name='casi_reali'
    )

    class Meta:
        db_table = 'caso_reale'

    def __str__(self):
        return self.nome_incidente


# ---------------------------------------------------------------------------
# Articolo
# ---------------------------------------------------------------------------

class Articolo(models.Model):
    id_articolo = models.AutoField(primary_key=True)
    titolo = models.CharField(max_length=300)
    testo = models.TextField()
    data_pubblicazione = models.DateField(auto_now_add=True)
    id_autore = models.ForeignKey(
        Utenti, on_delete=models.PROTECT,
        db_column='id_autore', related_name='articoli'
    )

    class Meta:
        db_table = 'articolo'

    def __str__(self):
        return self.titolo


# ---------------------------------------------------------------------------
# Interazione — superclasse della seconda generalizzazione (totale, esclusiva)
# ---------------------------------------------------------------------------

TIPO_INTERAZIONE_CHOICES = [
    ('like', 'Like'),
    ('commento', 'Commento'),
    ('segnalazione', 'Segnalazione'),
]


class Interazione(models.Model):
    id_interazione = models.AutoField(primary_key=True)
    tipo = models.CharField(max_length=12, choices=TIPO_INTERAZIONE_CHOICES)
    testo_commento = models.TextField(null=True, blank=True)
    data = models.DateTimeField(auto_now_add=True)
    id_utente = models.ForeignKey(
        Utenti, on_delete=models.CASCADE,
        db_column='id_utente', related_name='interazioni'
    )

    class Meta:
        db_table = 'interazione'

    def __str__(self):
        return f'{self.tipo} — {self.id_utente.username}'


# Sottoclassi Interazione

class InterazioneAttacco(models.Model):
    interazione = models.OneToOneField(
        Interazione, on_delete=models.CASCADE,
        primary_key=True, related_name='attacco_target'
    )
    id_attacco = models.ForeignKey(
        Attacco, on_delete=models.CASCADE,
        db_column='id_attacco', related_name='interazioni'
    )

    class Meta:
        db_table = 'interazione_attacco'


class InterazioneArticolo(models.Model):
    interazione = models.OneToOneField(
        Interazione, on_delete=models.CASCADE,
        primary_key=True, related_name='articolo_target'
    )
    id_articolo = models.ForeignKey(
        Articolo, on_delete=models.CASCADE,
        db_column='id_articolo', related_name='interazioni'
    )

    class Meta:
        db_table = 'interazione_articolo'


class InterazioneCaso(models.Model):
    interazione = models.OneToOneField(
        Interazione, on_delete=models.CASCADE,
        primary_key=True, related_name='caso_target'
    )
    id_caso = models.ForeignKey(
        CasoReale, on_delete=models.CASCADE,
        db_column='id_caso', related_name='interazioni'
    )

    class Meta:
        db_table = 'interazione_caso'


# ---------------------------------------------------------------------------
# Relazioni M:N
# ---------------------------------------------------------------------------

EFFICACIA_CHOICES = [
    ('bassa', 'Bassa'),
    ('media', 'Media'),
    ('alta', 'Alta'),
]


class Sfrutta(models.Model):
    id_attacco = models.ForeignKey(
        Attacco, on_delete=models.CASCADE, db_column='id_attacco'
    )
    id_vulnerabilita = models.ForeignKey(
        Vulnerabilita, on_delete=models.CASCADE, db_column='id_vulnerabilita'
    )

    class Meta:
        db_table = 'sfrutta'
        unique_together = [('id_attacco', 'id_vulnerabilita')]


class Mitiga(models.Model):
    id_contromisura = models.ForeignKey(
        Contromisura, on_delete=models.CASCADE, db_column='id_contromisura'
    )
    id_attacco = models.ForeignKey(
        Attacco, on_delete=models.CASCADE, db_column='id_attacco'
    )
    efficacia = models.CharField(max_length=6, choices=EFFICACIA_CHOICES)

    class Meta:
        db_table = 'mitiga'
        unique_together = [('id_contromisura', 'id_attacco')]


class Seguito(models.Model):
    id_seguito = models.AutoField(primary_key=True)
    id_seguace = models.ForeignKey(
        Utenti, on_delete=models.CASCADE,
        related_name='following', db_column='id_seguace'
    )
    id_utente_seguito = models.ForeignKey(
        Utenti, on_delete=models.CASCADE,
        related_name='followers', db_column='id_utente_seguito'
    )

    class Meta:
        db_table = 'seguito'
        unique_together = [('id_seguace', 'id_utente_seguito')]
        constraints = [
            models.CheckConstraint(
                check=~Q(id_seguace=F('id_utente_seguito')),
                name='no_self_follow'
            )
        ]
