from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.timezone import now

from sosfrene_client.forms import (
    ConnexionForm, MessageForm, SpanRequiredForm
)
from sosfrene_admin.forms import (
    EnregistrementForm, TraiterSignalementForm,
    SpecimenForm, NouvelleActiviteForm
)
from sosfrene_client.forms import MessageForm
from sosfrene_admin.constants import ADMIN_BASE, ADMIN_LOGIN_URL
from sosfrene_core.api import (
    messages_utilisateur, envoyer_message, creer_activite, ajouter_specimen
)
from sosfrene_core.constants import ETATS_SPECIMEN, ATTEINT
from sosfrene_core.models import (
    Utilisateur, Photo, Signalement, Message, Activite, Specimen, Localisation)


class AdminView(View):

    def get_context_data(self):
        context = {}
        context["menu_utilisateur"] = "sosfrene_admin/menu.html"
        context["route_base"] = "admin:"
        return context

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            utilisateur = Utilisateur.objects.get(user=request.user)
            if not utilisateur.admin:
                logout(request)
                redirect("admin:connexion")

        return super(AdminView, self).dispatch(request, *args, **kwargs)


class TableauBordView(LoginRequiredMixin, AdminView):
    login_url = ADMIN_LOGIN_URL

    def get(self, request):
        context = self.get_context_data()
        context["menu"] = "tableau"
        return render(
            request, ADMIN_BASE + "tableau_bord.html", context)


class AdministrateursView(LoginRequiredMixin, AdminView):
    login_url = ADMIN_LOGIN_URL

    def get(self, request):
        context = self.get_context_data()
        context["menu"] = "gestion"
        return render(
            request, ADMIN_BASE + "administrateurs.html", context)


class ConnexionView(AdminView):
    form_class = ConnexionForm
    initial = {}

    def get(self, request):
        if request.user.is_authenticated():
            return redirect("admin:tableau_bord")

        form = self.form_class(initial=self.initial)
        context = self.get_context_data()
        context["form"] = form
        return render(request, ADMIN_BASE + "connexion.html", context)

    def post(self, request):
        context = self.get_context_data()
        form = self.form_class(request.POST)
        context["form"] = form
        if form.is_valid():
            user = authenticate(username=form.cleaned_data["email"],
                                password=form.cleaned_data["password"])
            if user is not None:
                utilisateur = Utilisateur.objects.get(user=user)
                if utilisateur.admin:
                    login(request, user)
                    return redirect("admin:tableau_bord")
                else:
                    logout(request)
                    redirect("admin:connexion")
            else:
                context["erreur_mdp"] = True
                return render(
                    request, ADMIN_BASE + "connexion.html", context)

        return render(request, ADMIN_BASE + "connexion.html", context)


class DeconnexionView(View):

    def get(self, request):
        logout(request)
        return redirect("admin:connexion")


class SpecimensView(LoginRequiredMixin, AdminView):
    login_url = ADMIN_LOGIN_URL

    def get(self, request):
        context = self.get_context_data()
        specimens = list(Specimen.objects.all())
        context["specimens"] = specimens
        context["entetes"] = ["Localisation", "État", "Signalement"]
        context["menu"] = "specimens"
        return render(request, ADMIN_BASE + "specimens.html", context)


class NouveauSpecimenView(LoginRequiredMixin, AdminView):
    login_url = ADMIN_LOGIN_URL
    form_class = SpecimenForm
    initial = {}

    def get(self, request):
        context = self.get_context_data()
        form = self.form_class(initial=self.initial)
        context["form"] = form
        context["menu"] = "specimens"
        return render(request, ADMIN_BASE + "nouveau_specimen.html", context)

    def post(self, request):
        form = self.form_class(request.POST)
        context = self.get_context_data()
        context["menu"] = "specimens"
        context["form"] = form
        if form.is_valid():
            ajouter_specimen(form.cleaned_data["etat"],
                             form.cleaned_data["latitude"],
                             form.cleaned_data["longitude"])
            context["reussite"] = True
            form = self.form_class(initial=self.initial)
            context["form"] = form
            return render(request, ADMIN_BASE + "nouveau_specimen.html", context)

        return render(request, ADMIN_BASE + "nouveau_specimen.html", context)


class DetailsSpecimenView(LoginRequiredMixin, AdminView):
    login_url = ADMIN_LOGIN_URL
    form_class = SpecimenForm
    initial = {}

    def get(self, request, specimen_id):
        context = self.get_context_data()
        specimen = Specimen.objects.get(id=specimen_id)
        context["entetes"] = ["Date", "Nouvel état"]
        context["specimen"] = specimen
        activites = list(Activite.objects.filter(
            specimen__id=specimen.id).order_by("-date"))
        context["activites"] = activites
        context["menu"] = "specimens"
        self.initial["etat"] = specimen.etat
        self.initial["latitude"] = specimen.localisation.latitude
        self.initial["longitude"] = specimen.localisation.longitude
        form = self.form_class(initial=self.initial)
        context["form"] = form
        return render(request, ADMIN_BASE + "details_specimen.html", context)


class SupprimerSpecimenView(LoginRequiredMixin, AdminView):
    login_url = ADMIN_LOGIN_URL

    def get(self, request, specimen_id):
        context = self.get_context_data()
        specimen = Specimen.objects.get(id=specimen_id)
        specimen.delete()
        specimens = Specimen.objects.all()
        context["specimens"] = specimens
        context["entetes"] = ["Localisation", "État", "Signalement"]
        context["menu"] = "specimens"
        context["supprimer"] = True
        context["id"] = specimen_id
        return render(request, ADMIN_BASE + "specimens.html", context)


class MessagesView(LoginRequiredMixin, AdminView):
    login_url = ADMIN_LOGIN_URL

    def get(self, request):
        context = self.get_context_data()
        context["entetes"] = ["Date", "Expéditeur", "Sujet"]
        context["messages"] = messages_utilisateur(request.user.email)
        context["menu"] = "messages"
        return render(request, ADMIN_BASE + "messages.html", context)


class DetailsMessageView(LoginRequiredMixin, AdminView):
    login_url = ADMIN_LOGIN_URL

    def get(self, request, message_id):
        context = self.get_context_data()
        message = Message.objects.get(id=message_id)
        context["message"] = message
        context["menu"] = "messages"
        return render(request, ADMIN_BASE + "details_message.html", context)


class ReponseMessageView(LoginRequiredMixin, AdminView):
    login_url = ADMIN_LOGIN_URL
    form_class = MessageForm
    initial = {}

    def post(self, request, message_id):
        form = self.form_class(request.POST)
        if form.is_valid():
            message_original = Message.objects.get(id=message_id)
            envoyer_message(message_original.receveur, message_original.expediteur,
                            form.cleaned_data["sujet"],
                            form.cleaned_data["message"])
            form = self.form_class(initial=self.initial)
            context = self.get_context_data()
            context["message"] = message_original
            context["form"] = form
            context["reussite"] = True
            return render(
                request, ADMIN_BASE + "reponse_message.html", context)

    def get(self, request, message_id):
        context = self.get_context_data()
        message = Message.objects.get(id=message_id)
        self.initial["sujet"] = message.sujet
        form = self.form_class(initial=self.initial)
        context["form"] = form
        context["message"] = message
        context["menu"] = "messages"
        return render(request, ADMIN_BASE + "reponse_message.html", context)


class SignalementsView(LoginRequiredMixin, AdminView):
    login_url = ADMIN_LOGIN_URL

    def get(self, request):
        context = self.get_context_data()
        self._fill_context(context)
        return render(request, ADMIN_BASE + "signalements.html", context)

    def _fill_context(self, context):
        entetes = ["Date", "Localisation", "État", "# Spécimen"]
        context["entetes"] = entetes
        context["signalements"] =\
            list(Signalement.objects.all().order_by("-date"))
        context["menu"] = "signalements"


class DetailsSignalementView(LoginRequiredMixin, AdminView):
    login_url = ADMIN_LOGIN_URL

    def get(self, request, signalement_id):
        context = self.get_context_data()
        self._fill_context(context, signalement_id)
        return render(request, ADMIN_BASE + "details_signalement.html", context)

    def _fill_context(self, context, signalement_id):
        try:
            signalement = Signalement.objects.get(id=signalement_id)
            context["menu"] = "signalements"
            context["signalement"] = signalement
            photos = list(Photo.objects.filter(
                detailsignalement__signalement=signalement))
            context["photos"] = photos
        except Signalement.DoesNotExist:
            return


class TraiterSignalementView(LoginRequiredMixin, AdminView):
    login_url = ADMIN_LOGIN_URL
    form_class = TraiterSignalementForm
    initial = {"statut_specimen": ""}

    def get(self, request, signalement_id):
        context = self.get_context_data()
        context["menu"] = "signalements"
        context["traiter"] = False
        form = self.form_class(initial=self.initial)
        signalement = Signalement.objects.get(id=signalement_id)
        context["signalement"] = signalement
        context["utilisateur"] = signalement.utilisateur
        context["form"] = form
        return render(request, "traiter_signalement.html", context)

    def post(self, request, signalement_id):
        form = self.form_class(request.POST)
        context = self.get_context_data()
        context["traiter"] = False
        if form.is_valid():
            try:
                signalement = Signalement.objects.get(id=signalement_id)
            except Signalement.DoesNotExist:
                signalement = None

            if signalement:
                context["signalement"] = signalement
                context["traiter"] = True
                self._traiter(request.user, signalement, form)
                return render(
                    request, "traiter_signalement.html", context)
            else:
                pass
        else:
            context["erreur"] = True
            return render(
                request, "traiter_signalement.html", context)

    def _traiter(self, user, signalement, form):
        signalement.accepte = True
        confirme = form.cleaned_data["statut_specimen"]
        if confirme:
            signalement.specimen =\
                ajouter_specimen(ATTEINT, signalement.localisation.latitude,
                                 signalement.localisation.longitude)
            signalement.save()
            creer_activite("Le spécimen a été associé au signalement "
                           "et diagnostiqué comme étant atteint.",
                           signalement.specimen)

        envoyer_message(Utilisateur.objects.get(user=user),
                        signalement.utilisateur,
                        "Traitement de votre signalement",
                        form.cleaned_data["message"])


class NouvelleActiviteView(LoginRequiredMixin, AdminView):
    login_url = ADMIN_LOGIN_URL
    form_class = NouvelleActiviteForm
    initial = {}

    def get(self, request, specimen_id):
        form = self.form_class(initial=self.initial)
        context = self.get_context_data()
        context["form"] = form
        specimen = Specimen.objects.get(id=specimen_id)
        context["specimen"] = specimen
        context["menu"] = "specimens"
        return render(request, ADMIN_BASE + "activite.html", context)

    def post(self, request, specimen_id):
        context = self.get_context_data()
        form = self.form_class(request.POST)
        specimen = Specimen.objects.get(id=specimen_id)
        context["specimen"] = specimen
        if form.is_valid():
            try:
                specimen = Specimen.objects.get(id=specimen_id)
                specimen.etat = ETATS_SPECIMEN[int(form.cleaned_data["etat"])]
                specimen.save()
                creer_activite(form.cleaned_data["description"], specimen)
                context["reussite"] = True
                form = self.form_class(initial=self.initial)
                context["form"] = form
                return render(request, ADMIN_BASE + "activite.html", context)
            except Exception:
                context["erreur"] = True
                context["form"] = form
                return render(
                    request, ADMIN_BASE + "activite.html", context)
