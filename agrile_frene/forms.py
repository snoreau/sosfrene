from django import forms
from django.core.exceptions import ValidationError

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Div, ButtonHolder, Field

from .api import courriel_existe


class SpanRequiredForm(forms.Form):
    def clean_required(self, field_data, message="Ce champ est requis."):
        if field_data == "":
            raise ValidationError(message)


class EnregistrementForm(SpanRequiredForm):
    first_name = forms.CharField(label="Prénom", max_length=80, required=False)
    last_name = forms.CharField(label="Nom", max_length=80, required=False)
    email = forms.EmailField(label="Courriel", max_length=80, required=False)
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput,
                               max_length=80, required=False)
    confirm_password = forms.CharField(
        label="Confirmez votre mot de passe",
        widget=forms.PasswordInput,
        max_length=80, required=False)

    def __init__(self, *args, **kwargs):
        super(EnregistrementForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'form-enregistrement'
        self.helper.form_method = 'post'
        self.helper.form_action = 'enregistrement'
        self.helper.add_input(Submit('submit', 'Créer un compte', css_class="btn-block"))
        self.helper.error_text_inline = False

    def clean_first_name(self):
        self.clean_required(self.cleaned_data["first_name"])
        return self.cleaned_data["first_name"]

    def clean_last_name(self):
        self.clean_required(self.cleaned_data["last_name"])
        return self.cleaned_data["last_name"]

    def clean_email(self):
        self.clean_required(self.cleaned_data["email"])
        if courriel_existe(self.cleaned_data["email"]):
            raise ValidationError("Cette adresse courriel est déjà utilisée.")
        return self.cleaned_data["email"]

    def clean_password(self):
        self.clean_required(self.cleaned_data["password"])
        return self.cleaned_data["password"]

    def clean_confirm_password(self):
        self.clean_required(self.cleaned_data["confirm_password"])

        if self.cleaned_data["password"] !=\
                self.cleaned_data["confirm_password"]:
            raise ValidationError('Les mots de passe doivent être identiques.')

        return self.cleaned_data["confirm_password"]


class ConnexionForm(SpanRequiredForm):
    email = forms.CharField(label="Courriel", max_length=80, required=False)
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput,
                               max_length=80, required=False)

    def __init__(self, *args, **kwargs):
        super(ConnexionForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'form-connexion'
        self.helper.form_method = 'post'
        self.helper.form_action = 'connexion'
        self.helper.add_input(Submit('submit', 'Se connecter', css_class="btn-block"))
        self.helper.error_text_inline = False

    def clean_email(self):
        self.clean_required(self.cleaned_data["email"])
        if not courriel_existe(self.cleaned_data["email"]):
            raise ValidationError(
                "Aucun utilisateur avec cette adresse n'a été trouvé.")
        return self.cleaned_data["email"]

    def clean_password(self):
        self.clean_required(self.cleaned_data["password"])
        return self.cleaned_data["password"]


class SignalementForm(SpanRequiredForm):
    description = forms.CharField(
        widget=forms.Textarea, label="Description", max_length=500, required=False)
    longitude = forms.FloatField(widget=forms.HiddenInput())
    latitude = forms.FloatField(widget=forms.HiddenInput())
    photos_pks = forms.CharField(widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        super(SignalementForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'form-nouveau-signalement'
        self.helper.form_method = 'post'
        self.helper.form_action = 'nouveau_signalement'
        self.helper.error_text_inline = False
        self.helper.layout = Layout(
            "longitude", "latitude", "photos_pks", "description")


class ProfilForm(forms.Form):
    notifications = forms.BooleanField(
        label="Reçevoir les notifications par courriel", required=False)

    def __init__(self, *args, **kwargs):
        super(ProfilForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'form-profil'
        self.helper.form_method = 'post'
        self.helper.form_action = 'profil'
        self.helper.add_input(Submit(
            'submit', 'Enregistrer', css_id="btn-enregistrer-profil"))
