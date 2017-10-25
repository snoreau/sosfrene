from django.views import View
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.timezone import now
from django.http import HttpResponseRedirect

from agrile_frene.forms import (
    EnregistrementForm, AdminConnexionForm,
    MessageForm, ProfilForm, TraiterSignalementForm)
from agrile_frene.models import (
    Utilisateur, Photo, Signalement, Message, Activite, Specimen)
from agrile_frene.api import messages_utilisateur
from agrile_frene.constants import ETATS_SPECIMEN, ATTEINT


def valider_permission(user):
    utilisateur = Utilisateur.objects.get(user=user)
    if utilisateur.admin:
        return True
    else:
        return False


class TableauBordView(LoginRequiredMixin, View):
    login_url = "/admin/connexion/"

    def get(self, request):
        if not valider_permission(request.user):
            logout(request)
            return redirect("connexion_admin")

        return render(request, "admin/tableau_bord.html", {"user": request.user})


class ConnexionView(View):
    form_class = AdminConnexionForm
    initial = {}

    def get(self, request):
        if request.user.is_authenticated():
            return redirect("tableau_bord")

        form = self.form_class(initial=self.initial)
        context = {}
        context["form"] = form
        return render(request, "admin/connexion.html", context)

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data["email"],
                                password=form.cleaned_data["password"])
            if user is not None:
                utilisateur = Utilisateur.objects.get(user=user)
                if utilisateur.admin:
                    login(request, user)
                    return redirect("tableau_bord")
            else:
                return render(request, "admin/connexion.html",
                              {'form': form, "erreur_mdp": True})

        return render(request, "admin/connexion.html", {'form': form})


class DeconnexionView(View):
    def get(self, request):
        logout(request)
        return redirect("connexion_admin")


class ActivitesView(LoginRequiredMixin, View):
    login_url = "/admin/connexion/"

    def get(self, request):
        if not valider_permission(request.user):
            logout(request)
            return redirect("connexion_admin")
        pass


class UtilisateursView(LoginRequiredMixin, View):
    login_url = "/admin/connexion/"
    form_class = EnregistrementForm
    initial = {}

    def get(self, request):
        if not valider_permission(request.user):
            logout(request)
            return redirect("connexion_admin")

        if request.user.is_authenticated():
            return redirect("tableau_bord")

        form = self.form_class(initial=self.initial)
        context = {}
        context["form"] = form
        return render(request, "enregistrement.html", context)

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
                logger.exception(
                    "Une erreur est survenue lors de la création du compte.")
                return render(
                    request, "enregistrement.html",
                    {'form': form, "erreur": True})

            form = self.form_class(initial=self.initial)
            return render(request, "enregistrement.html",
                          {'form': form, "reussite": True})
        return render(
            request, "enregistrement.html", {'form': form})


class SpecimensView(LoginRequiredMixin, View):
    login_url = "/admin/connexion/"

    def get(self, request):
        if not valider_permission(request.user):
            logout(request)
            return redirect("connexion_admin")
        context = {}
        context["specimens"] = specimens
        context["entetes"] = ["Latitude", "Longitude", "État", "Signalement"]
        return render(request, "admin/specimens.html", context)


class MessagesView(LoginRequiredMixin, View):
    login_url = "/admin/connexion/"

    def get(self, request):
        if not valider_permission(request.user):
            logout(request)
            return redirect("connexion_admin")
        context = {}
        context["entetes"] = ["Date", "Expéditeur", "Sujet"]
        context["messages"] = messages_utilisateur(request.user.email)
        return render(request, "admin/messages.html", context)


class DetailsMessageView(LoginRequiredMixin, View):
    login_url = '/admin/connexion/'

    def get(self, request, message_id):
        if not valider_permission(request.user):
            logout(request)
            return redirect("connexion_admin")
        context = {}
        message = Message.objects.get(id=message_id)
        context["message"] = message
        return render(request, "admin/details_message.html", context)


class ReponseMessageView(LoginRequiredMixin, View):
    login_url = '/admin/connexion/'
    form_class = MessageForm
    initial = {}

    def get(self, request, message_id):
        if not valider_permission(request.user):
            logout(request)
            return redirect("connexion_admin")
        form = self.form_class(initial=self.initial)
        context = {}
        context["form"] = form
        message = Message.objects.get(id=message_id)
        context["message"] = message
        return render(request, "reponse_message.html", context)

    def post(self, request, message_id):
        form = self.form_class(request.POST)
        if form.is_valid():
            message_original = Message.objects.get(id=message_id)
            contenu = form.cleaned_data["message"]
            nouveau_message = Message()
            nouveau_message.contenu = contenu
            nouveau_message.expediteur = message_original.receveur
            nouveau_message.receveur = message_original.expediteur
            nouveau_message.sujet = message_original.sujet
            nouveau_message.date = now()
            nouveau_message.save()
            form = self.form_class(initial=self.initial)
            context = {}
            context["message"] = message_original
            context["form"] = form
            context["reussite"] = True
            return render(
                request, "admin/reponse_message.html", context)


class SignalementsView(LoginRequiredMixin, View):
    login_url = "/admin/connexion/"

    def get(self, request):
        if not valider_permission(request.user):
            logout(request)
            return redirect("connexion_admin")
        context = {}
        self._fill_context(context)
        return render(request, "admin/signalements.html", context)

    def _fill_context(self, context):
        entetes = ["Date", "Localisation", "État", "# Spécimen"]
        context["entetes"] = entetes
        context["signalements"] = Signalement.objects.all()


class DetailsSignalementView(LoginRequiredMixin, View):
    login_url = '/admin/connexion/'

    def get(self, request, signalement_id):
        context = {}
        self._fill_context(context, signalement_id)
        return render(request, "admin/details_signalement.html", context)

    def _fill_context(self, context, signalement_id):
        try:
            signalement = Signalement.objects.get(id=signalement_id)
            context["signalement"] = signalement
            photos = Photo.objects.filter(
                detailsignalement__signalement=signalement)
            context["photos"] = photos
        except Signalement.DoesNotExist:
            return


class TraiterSignalementView(LoginRequiredMixin, View):
    login_url = '/admin/connexion/'
    form_class = TraiterSignalementForm
    initial = {"statut_specimen": ""}

    def get(self, request, signalement_id):
        context = {}
        context["traiter"] = False
        form = self.form_class(initial=self.initial)
        signalement = Signalement.objects.get(id=signalement_id)
        context["signalement"] = signalement
        context["utilisateur"] = signalement.utilisateur
        context["form"] = form
        return render(request, "admin/traiter_signalement.html", context)

    def post(self, request, signalement_id):
        form = self.form_class(request.POST)
        context = {}
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
                    request, "admin/traiter_signalement.html", context)
            else:
                pass
        else:
            context["erreur"] = True
            return render(
                request, "admin/traiter_signalement.html", context)

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
        message_signalement.save()


class ProfilView(View):
    login_url = "/admin/connexion/"
    form_class = ProfilForm
    initial = {}

    def get(self, request):
        if not valider_permission(request.user):
            logout(request)
            return redirect("connexion_admin")
        self._remplir_initial(request.user)
        form = self.form_class(initial=self.initial)
        context = {}
        context["form"] = form
        context["user"] = request.user
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
