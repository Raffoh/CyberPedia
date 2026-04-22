import re
from django import forms
from django.core.exceptions import ValidationError

from .models import (
    Utenti, Attacco, AttaccoRete, AttaccoWeb, AttaccoSocial, AttaccoMalware,
    Vulnerabilita, Contromisura, CasoReale, Articolo,
)


# ---------------------------------------------------------------------------
# Auth
# ---------------------------------------------------------------------------

class RegistrazioneForm(forms.Form):
    username = forms.CharField(max_length=20, min_length=3)
    email = forms.EmailField()
    password1 = forms.CharField(widget=forms.PasswordInput, label='Password')
    password2 = forms.CharField(widget=forms.PasswordInput, label='Conferma password')

    def clean_username(self):
        username = self.cleaned_data['username']
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            raise ValidationError('Solo lettere, numeri e underscore.')
        if Utenti.objects.filter(username=username).exists():
            raise ValidationError('Username già in uso.')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if Utenti.objects.filter(email=email).exists():
            raise ValidationError('Email già registrata.')
        return email

    def clean_password1(self):
        pwd = self.cleaned_data.get('password1', '')
        if len(pwd) < 8:
            raise ValidationError('La password deve avere almeno 8 caratteri.')
        if not re.search(r'[0-9]', pwd):
            raise ValidationError('La password deve contenere almeno un numero.')
        if not re.search(r'[A-Z]', pwd):
            raise ValidationError('La password deve contenere almeno una lettera maiuscola.')
        if not re.search(r'[^a-zA-Z0-9]', pwd):
            raise ValidationError('La password deve contenere almeno un simbolo.')
        return pwd

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get('password1')
        p2 = cleaned.get('password2')
        if p1 and p2 and p1 != p2:
            self.add_error('password2', 'Le password non coincidono.')
        return cleaned


class LoginForm(forms.Form):
    username = forms.CharField(max_length=20)
    password = forms.CharField(widget=forms.PasswordInput)


# ---------------------------------------------------------------------------
# Attacco
# ---------------------------------------------------------------------------

class AttaccoBaseForm(forms.ModelForm):
    class Meta:
        model = Attacco
        fields = ['nome', 'descrizione', 'severita', 'data_pubblicazione',
                  'riferimento_mitre', 'immagine']
        widgets = {
            'data_pubblicazione': forms.DateInput(attrs={'type': 'date'}),
            'descrizione': forms.Textarea(attrs={'rows': 5}),
        }


class AttaccoReteForm(forms.ModelForm):
    class Meta:
        model = AttaccoRete
        fields = ['protocollo', 'porta_bersaglio', 'livello_osi']


class AttaccoWebForm(forms.ModelForm):
    class Meta:
        model = AttaccoWeb
        fields = ['tipo_injection', 'owasp_category', 'url_esempio']


class AttaccoSocialForm(forms.ModelForm):
    class Meta:
        model = AttaccoSocial
        fields = ['canale', 'leva_psicologica']


class AttaccoMalwareForm(forms.ModelForm):
    class Meta:
        model = AttaccoMalware
        fields = ['tipo_payload', 'persistenza', 'propagazione']


# ---------------------------------------------------------------------------
# Entita secondarie
# ---------------------------------------------------------------------------

class VulnerabilitaForm(forms.ModelForm):
    class Meta:
        model = Vulnerabilita
        fields = ['codice_cve', 'descrizione', 'cvss_score',
                  'software_affetto', 'anno_scoperta']
        widgets = {'descrizione': forms.Textarea(attrs={'rows': 4})}

    def clean_cvss_score(self):
        score = self.cleaned_data['cvss_score']
        if score < 0 or score > 10:
            raise ValidationError('Il CVSS score deve essere tra 0 e 10.')
        return score

    def clean_anno_scoperta(self):
        anno = self.cleaned_data['anno_scoperta']
        if anno < 1980:
            raise ValidationError('Anno non valido (minimo 1980).')
        return anno


class ContromisuraForm(forms.ModelForm):
    class Meta:
        model = Contromisura
        fields = ['nome', 'descrizione', 'tipo']
        widgets = {'descrizione': forms.Textarea(attrs={'rows': 4})}


class CasoRealeForm(forms.ModelForm):
    class Meta:
        model = CasoReale
        fields = ['nome_incidente', 'anno', 'vittima',
                  'danno_stimato_usd', 'descrizione_breve', 'id_attacco']
        widgets = {'descrizione_breve': forms.Textarea(attrs={'rows': 4})}


class ArticoloForm(forms.ModelForm):
    class Meta:
        model = Articolo
        fields = ['titolo', 'testo']
        widgets = {'testo': forms.Textarea(attrs={'rows': 10})}


class ProfiloForm(forms.ModelForm):
    class Meta:
        model = Utenti
        fields = ['bio', 'foto_profilo']
        widgets = {'bio': forms.Textarea(attrs={'rows': 4})}
