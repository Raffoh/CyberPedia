from django.contrib import admin
from .models import (
    Utenti, Attacco, AttaccoRete, AttaccoWeb, AttaccoSocial, AttaccoMalware,
    Vulnerabilita, Contromisura, CasoReale, Articolo,
    Interazione, InterazioneAttacco, InterazioneArticolo, InterazioneCaso,
    Sfrutta, Mitiga, Seguito,
)


class AttaccoReteInline(admin.StackedInline):
    model = AttaccoRete
    extra = 0


class AttaccoWebInline(admin.StackedInline):
    model = AttaccoWeb
    extra = 0


class AttaccoSocialInline(admin.StackedInline):
    model = AttaccoSocial
    extra = 0


class AttaccoMalwareInline(admin.StackedInline):
    model = AttaccoMalware
    extra = 0


class SfruttaInline(admin.TabularInline):
    model = Sfrutta
    extra = 1


class MitigaInline(admin.TabularInline):
    model = Mitiga
    extra = 1


@admin.register(Attacco)
class AttaccoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'severita', 'data_pubblicazione', 'id_autore', 'get_famiglia']
    list_filter = ['severita', 'data_pubblicazione']
    search_fields = ['nome', 'descrizione']
    inlines = [AttaccoReteInline, AttaccoWebInline,
               AttaccoSocialInline, AttaccoMalwareInline,
               SfruttaInline, MitigaInline]

    def get_famiglia(self, obj):
        return obj.get_famiglia()
    get_famiglia.short_description = 'Famiglia'


@admin.register(Utenti)
class UtentiAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'livello', 'data_registrazione']
    list_filter = ['livello']
    search_fields = ['username', 'email']


@admin.register(Vulnerabilita)
class VulnerabilitaAdmin(admin.ModelAdmin):
    list_display = ['codice_cve', 'software_affetto', 'cvss_score', 'anno_scoperta']
    list_filter = ['anno_scoperta']
    search_fields = ['codice_cve', 'software_affetto']


@admin.register(Contromisura)
class ContromisuraAdmin(admin.ModelAdmin):
    list_display = ['nome', 'tipo']
    list_filter = ['tipo']


@admin.register(CasoReale)
class CasoRealeAdmin(admin.ModelAdmin):
    list_display = ['nome_incidente', 'vittima', 'anno', 'danno_stimato_usd']
    list_filter = ['anno']
    search_fields = ['nome_incidente', 'vittima']


@admin.register(Articolo)
class ArticoloAdmin(admin.ModelAdmin):
    list_display = ['titolo', 'id_autore', 'data_pubblicazione']
    search_fields = ['titolo']


@admin.register(Interazione)
class InterazioneAdmin(admin.ModelAdmin):
    list_display = ['tipo', 'id_utente', 'data']
    list_filter = ['tipo']


admin.site.register(AttaccoRete)
admin.site.register(AttaccoWeb)
admin.site.register(AttaccoSocial)
admin.site.register(AttaccoMalware)
admin.site.register(InterazioneAttacco)
admin.site.register(InterazioneArticolo)
admin.site.register(InterazioneCaso)
admin.site.register(Sfrutta)
admin.site.register(Mitiga)
admin.site.register(Seguito)
