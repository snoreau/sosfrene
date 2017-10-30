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
    EnregistrementForm, ProfilForm, TraiterSignalementForm,
    SpecimenForm, NouvelleActiviteForm
)
from sosfrene_client.forms import MessageForm
from sosfrene_admin.constants import ADMIN_BASE, ADMIN_LOGIN_URL
from sosfrene_core.models import (
    Utilisateur, Photo, Signalement, Message, Activite, Specimen, Localisation)
from sosfrene_core.api import messages_utilisateur
from sosfrene_core.constants import ETATS_SPECIMEN, ATTEINT


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
                context["erreur_mdp"] = True
                return render(
                    request, ADMIN_BASE + "connexion.html", context)

        return render(request, ADMIN_BASE + "connexion.html", context)


class DeconnexionView(View):

    def get(self, request):
        logout(request)
        return redirect("admin:connexion")


class ActivitesView(LoginRequiredMixin, AdminView):
    login_url = ADMIN_LOGIN_URL

    def get(self, request):
        pass


class UtilisateursView(LoginRequiredMixin, AdminView):
    login_url = ADMIN_LOGIN_URL
    form_class = EnregistrementForm
    initial = {}

    def get(self, request):
        pass

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            try:
                user = User.objects.create_user(
                    form.cleaned_data["email"],
                    password=form.cleaned_data["password"])
                nouvel_utilisateur = Utilisateur()
                user.first_name = form.cleaned_data["first_name"]
                user.last_name = form.cleaned_data["last_name"]
                user.email = form.cleaned_data["email"]
                user.save()
                nouvel_utilisateur.user = user
                nouvel_utilisateur.notifications = False
                nouvel_utilisateur.save()
            except Exception:
                return render(
                    request, "enregistrement.html",
                    {'form': form, "erreur": True})

            form = self.form_class(initial=self.initial)
            return render(request, "enregistrement.html",
                          {'form': form, "reussite": True})
        return render(
            request, "enregistrement.html", {'form': form})


class SpecimensView(LoginRequiredMixin, AdminView):
    login_url = ADMIN_LOGIN_URL

    def get(self, request):
        context = self.get_context_data()
        specimens = Specimen.objects.all()
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
            specimen = Specimen()
            specimen.etat = ETATS_SPECIMEN[int(form.cleaned_data["etat"])]
            localisation = Localisation()
            localisation.latitude = form.cleaned_data["latitude"]
            localisation.longitude = form.cleaned_data["longitude"]
            localisation.save()
            specimen.localisation = localisation
            specimen.save()
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
        activites = Activite.objects.filter(specimen__id=specimen.id)
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
            contenu = form.cleaned_data["message"]
            nouveau_message = Message()
            nouveau_message.contenu = contenu
            nouveau_message.expediteur = message_original.receveur
            nouveau_message.receveur = message_original.expediteur
            nouveau_message.sujet = form.cleaned_data["sujet"]
            nouveau_message.date = now()
            nouveau_message.save()
            form = self.form_class(initial=self.initial)
            context = self.get_context_data()
            context["message"] = message_original
            context["form"] = form
            context["reussite"] = True
            return render(
                request, ADMIN_BASE + "reponse_message.html", context)

    def get(self, request, message_id):
        form = self.form_class(initial=self.initial)
        context = self.get_context_data()
        context["form"] = form
        message = Message.objects.get(id=message_id)
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
        context["signalements"] = Signalement.objects.all().order_by("-date")
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
            photos = Photo.objects.filter(
                detailsignalement__signalement=signalement)
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
            specimen = Specimen()
            specimen.localisation = signalement.localisation
            specimen.etat = ETATS_SPECIMEN[ATTEINT]
            specimen.save()
            signalement.specimen = specimen
            activite = Activite()
            activite.specimen = specimen
            activite.date = now()
            activite.description = "Spécimen associé au signalement."
        signalement.save()

        message = form.cleaned_data["message"]
        message_signalement = Message()
        message_signalement.date = now()
        message_signalement.expediteur = Utilisateur.objects.get(user=user)
        message_signalement.receveur = signalement.utilisateur
        message_signalement.contenu = message
        message_signalement.sujet = "Traitement du signalement"
        message_signalement.save()

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
                activite = Activite()
                activite.specimen = specimen
                activite.date = now()
                activite.description = form.cleaned_data["description"]
                activite.save()
                context["reussite"] = True
                form = self.form_class(initial=self.initial)
                context["form"] = form
                return render(request, ADMIN_BASE + "activite.html", context)
            except Exception:
                context["erreur"] = True
                context["form"] = form
                return render(
                    request, ADMIN_BASE + "activite.html", context)



class ProfilView(LoginRequiredMixin, AdminView):
    login_url = ADMIN_LOGIN_URL
    form_class = ProfilForm
    initial = {}

    def get(self, request):
        self._remplir_initial(request.user)
        form = self.form_class(initial=self.initial)
        context = self.get_context_data()
        context["form"] = form
        context["user"] = request.user
        context["menu"] = "profil"
        return render(request, "profil.html", context)

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            utilisateur = Utilisateur.objects.get(user=request.user)
            utilisateur.notifications = form.cleaned_data["notifications"]
            utilisateur.save()

            self._remplir_initial(request.user)
            form = self.form_class(initial=self.initial)
            return render(request, "profil.html", {'form': form, "reussite": True})
        return render(request, "profil.html", {'form': form})

    def _remplir_initial(self, user):
        utilisateur = Utilisateur.objects.get(user=user)
        self.initial["notifications"] = utilisateur.notifications
