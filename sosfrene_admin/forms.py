from django import forms
from django.core.exceptions import ValidationError

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from sosfrene_core.constants import ETATS_SPECIMEN
from sosfrene_core.api import courriel_existe
from sosfrene_client.forms import SpanRequiredForm


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


class TraiterSignalementForm(forms.Form):
    statut_specimen = forms.CharField(
        widget=forms.HiddenInput(), required=False)
    message = forms.CharField(
        widget=forms.Textarea, label="Message pour l'utilisateur:",
        max_length=1000, required=False)


class SpecimenForm(SpanRequiredForm):
    etat = forms.ChoiceField(
        label="État", choices=list(ETATS_SPECIMEN.items()), required=False)
    latitude = forms.FloatField(label="Latitude (-90 à 90)", required=False,
                                min_value=-90.0, max_value=90,
                                widget=forms.TextInput(
                                    attrs={'id': 'lat-input'}))
    longitude = forms.FloatField(label="Longitude (-180 à 180)", required=False,
                                 min_value=-180, max_value=180,
                                 widget=forms.TextInput(
                                     attrs={'id': 'lon-input'}))

    def __init__(self, *args, **kwargs):
        super(SpecimenForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'form-profil'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit(
            'submit', 'Enregistrer', css_id="btn-ajouter-specimen",
            css_class="btn-large"))

    def clean_latitude(self):
        self.clean_required(self.cleaned_data["latitude"])
        return self.cleaned_data["latitude"]

    def clean_longitude(self):
        self.clean_required(self.cleaned_data["longitude"])
        return self.cleaned_data["longitude"]


class NouvelleActiviteForm(SpanRequiredForm):
    etat = forms.ChoiceField(
        label="État", choices=list(ETATS_SPECIMEN.items()), required=False)
    description = forms.CharField(
        widget=forms.Textarea, label="Description", max_length=500, required=False)

    def __init__(self, *args, **kwargs):
        super(NouvelleActiviteForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'form-activite'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit(
            'submit', 'Soumettre', css_id="btn-ajouter-activite",
            css_class="btn-large"))

    def clean_latitude(self):
        self.clean_required(self.cleaned_data["description"])
        return self.cleaned_data["description"]
