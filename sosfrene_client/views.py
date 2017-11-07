import json
from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.utils import timezone
from django.utils.timezone import now

from sosfrene_client.forms import (
    EnregistrementForm, ConnexionForm, SignalementForm, ProfilForm, MessageForm
)
from sosfrene_core.models import (
    Utilisateur, Photo, Message, Signalement,
    DetailSignalement, Localisation, Notification
)
from sosfrene_core.api import (
    signalements_utilisateur, messages_utilisateur,
    specimens_carte, notifications_utilisateur, creer_signalement
)


class ClientView(View):

    def get_context_data(self):
        context = {}
        context["menu_utilisateur"] = "sosfrene_client/menu.html"
        context["route_base"] = "client:"
        return context


class AccueilView(ClientView):

    def get(self, request):
        context = self.get_context_data()
        return render(request, "accueil.html", context)


class CarteView(ClientView):

    def get(self, request):
        context = self.get_context_data()
        context["menu"] = "carte"
        return render(request, "carte.html", context)


class FreneView(ClientView):

    def get(self, request):
        context = self.get_context_data()
        context["menu"] = "frene"
        return render(request, "frene.html", context)


class AgrileView(ClientView):

    def get(self, request):
        context = self.get_context_data()
        context["menu"] = "agrile"
        return render(request, "agrile.html", context)


class SymptomesView(ClientView):

    def get(self, request):
        context = self.get_context_data()
        context["menu"] = "symptomes"
        return render(request, "symptomes.html", context)


class EnregistrementView(ClientView):
    form_class = EnregistrementForm
    initial = {}

    def get(self, request):
        if request.user.is_authenticated():
            return redirect("client:accueil")

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
                return render(
                    request, "enregistrement.html",
                    {'form': form, "erreur": True})

            form = self.form_class(initial=self.initial)
            return render(request, "enregistrement.html",
                          {'form': form, "reussite": True})
        return render(
            request, "enregistrement.html", {'form': form})


class ConnexionView(View):
    form_class = ConnexionForm
    initial = {}

    def get(self, request):
        if request.user.is_authenticated():
            return redirect("client:notifications")

        form = self.form_class(initial=self.initial)
        context = {}
        context["form"] = form
        return render(request, "connexion.html", context)

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data["email"],
                                password=form.cleaned_data["password"])
            if user is not None:
                login(request, user)
                return redirect("client:notifications")
            else:
                return render(request, "connexion.html",
                              {'form': form, "erreur_mdp": True})

        return render(request, "connexion.html", {'form': form})


class DeconnexionView(View):
    def get(self, request):
        logout(request)
        return redirect("client:accueil")


class SignalementsView(LoginRequiredMixin, ClientView):

    def get(self, request):
        context = self.get_context_data()
        context["menu"] = "signalements"
        self._fill_context(context, request.user)
        return render(request, "signalements.html", context)

    def _fill_context(self, context, user):
        entetes = ["Date", "Localisation", "État", "# Spécimen"]
        context["entetes"] = entetes
        context["signalements"] = signalements_utilisateur(user)

class DetailsSignalementView(LoginRequiredMixin, ClientView):

    def get(self, request, signalement_id):
        context = self.get_context_data()
        context["menu"] = "signalements"
        self._fill_context(context, signalement_id)
        if context["signalement"]:
            return render(
                request, "details_signalement.html", context)
        else:
            return redirect("client:signalements")

    def _fill_context(self, context, signalement_id):
        try:
            signalement = Signalement.objects.get(id=signalement_id)
            context["signalement"] = signalement
            photos = Photo.objects.filter(
                detailsignalement__signalement=signalement)
            context["photos"] = photos
        except Signalement.DoesNotExist:
            context["signalement"] = None


class NouveauSignalementView(LoginRequiredMixin, ClientView):
    form_class = SignalementForm
    initial = {"date": timezone.now()}

    def get(self, request):
        form = self.form_class(initial=self.initial)
        context = self.get_context_data()
        context["menu"] = "signalements"
        context["form"] = form
        return render(
            request, "nouveau_signalement.html", context)

    def post(self, request):
        form = self.form_class(request.POST)
        context = self.get_context_data()
        context["menu"] = "signalements"
        context["form"] = form
        if form.is_valid():
            try:
                creer_signalement(
                    form.cleaned_data["latitude"], form.cleaned_data["longitude"],
                    form.cleaned_data["description"], request.user,
                    form.cleaned_data["photos_pks"])

                form = self.form_class(initial=self.initial)
                context["form"] = form
                context["reussite"] = True
                return render(
                    request, "nouveau_signalement.html",
                    context)
            except Exception:
                context["erreur"] = True
                return render(
                    request, "nouveau_signalement.html",
                    context)
        else:
            render(request, "nouveau_signalement.html",
                   context)


class MessagesView(LoginRequiredMixin, ClientView):

    def get(self, request):
        context = self.get_context_data()
        context["menu"] = "messages"
        context["entetes"] = ["Date", "Expéditeur", "Sujet"]
        context["messages"] = messages_utilisateur(request.user.email)
        return render(request, "messages.html", context)


class DetailsMessageView(LoginRequiredMixin, ClientView):

    def get(self, request, message_id):
        context = self.get_context_data()
        context["menu"] = "messages"
        try:
            message = Message.objects.get(id=message_id)
        except Message.DoesNotExist:
            return redirect("client:messages")

        context["message"] = message
        return render(request, "details_message.html", context)


class ReponseMessageView(LoginRequiredMixin, ClientView):
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
                request, "reponse_message.html", context)

    def get(self, request, message_id):
        context = self.get_context_data()
        context["menu"] = "messages"
        try:
            message = Message.objects.get(id=message_id)
        except Message.DoesNotExist:
            return redirect("client:messages")

        self.initial["sujet"] = message.sujet
        form = self.form_class(initial=self.initial)
        context["form"] = form
        context["message"] = message
        return render(request, "reponse_message.html", context)


class ProfilView(LoginRequiredMixin, ClientView):
    form_class = ProfilForm
    initial = {}

    def get(self, request):
        self._remplir_initial(request.user)
        form = self.form_class(initial=self.initial)
        context = self.get_context_data()
        context["menu"] = "profil"
        context["form"] = form
        context["user"] = request.user
        return render(request, "profil.html", context)

    def post(self, request):
        context = self.get_context_data()
        form = self.form_class(request.POST)
        if form.is_valid():
            utilisateur = Utilisateur.objects.get(user=request.user)
            utilisateur.notifications = form.cleaned_data["notifications"]
            utilisateur.save()

            self._remplir_initial(request.user)
            form = self.form_class(initial=self.initial)
            context["reussite"] = True
            context["form"] = form
            return render(request, "profil.html", context)
        return render(request, "profil.html", context)

    def _remplir_initial(self, user):
        utilisateur = Utilisateur.objects.get(user=user)
        self.initial["notifications"] = utilisateur.notifications


class TelechargementView(LoginRequiredMixin, ClientView):

    def post(self, request):
        fichiers = request.FILES.getlist('file')
        data = {}
        pks = []
        for fichier in fichiers:
            photo = Photo()
            photo.source = fichier
            photo.save()
            pks.append(photo.pk)
        data = {"photos_pk": pks}
        return JsonResponse(data)


class SpecimensCarteView(LoginRequiredMixin, ClientView):

    def get(self, request):
        liste_specimens = specimens_carte()
        data = {"specimens": liste_specimens}
        return JsonResponse(data)


class NotificationsView(LoginRequiredMixin, ClientView):

    def get(self, request):
        context = self.get_context_data()
        context["menu"] = "notifications"
        context["notifications"] =\
            notifications_utilisateur(request.user.email)
        return render(request, "notifications.html", context)


class ArchiverNotificationView(LoginRequiredMixin, ClientView):

    def post(self, request):
        try:
            notification_id = request.POST["id"]
            notification = Notification.objects.get(id=notification_id)
            notification.archive = True
            notification.save()
        except Notification.DoesNotExist:
            data = {"reussite": False}

        data = {"reussite": True}
        return JsonResponse(data)
