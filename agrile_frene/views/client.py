import json
from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.utils import timezone
from django.utils.timezone import now
from agrile_frene.forms import (
    EnregistrementForm, ConnexionForm,
    SignalementForm, MessageForm, ProfilForm)
from agrile_frene.models import (
    Utilisateur, Photo, Message, Signalement, DetailSignalement, Localisation)
from agrile_frene.api import signalements_utilisateur, messages_utilisateur


class AccueilView(View):

    def get(self, request):
        return render(request, "accueil.html", {"user": request.user})


class EnregistrementView(View):
    form_class = EnregistrementForm
    initial = {}

    def get(self, request):
        if request.user.is_authenticated():
            return redirect("accueil")

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



class ConnexionView(View):
    form_class = ConnexionForm
    initial = {}

    def get(self, request):
        if request.user.is_authenticated():
            return redirect("signalements")

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
                return redirect("signalements")
            else:
                return render(request, "connexion.html",
                              {'form': form, "erreur_mdp": True})

        return render(request, "connexion.html", {'form': form})


class DeconnexionView(View):
    def get(self, request):
        logout(request)
        return redirect("accueil")


class SignalementsView(LoginRequiredMixin, View):
    login_url = '/connexion/'

    def get(self, request):
        context = {}
        self._fill_context(context, request.user)
        return render(request, "signalements.html", context)

    def _fill_context(self, context, user):
        entetes = ["Date", "Localisation", "État", "# Spécimen"]
        context["entetes"] = entetes
        context["signalements"] = signalements_utilisateur(user)

class DetailsSignalementView(LoginRequiredMixin, View):
    login_url = '/connexion/'

    def get(self, request, signalement_id):
        context = {}
        self._fill_context(context, signalement_id)
        return render(request, "details_signalement.html", context)

    def _fill_context(self, context, signalement_id):
        try:
            signalement = Signalement.objects.get(id=signalement_id)
            context["signalement"] = signalement
            photos = Photo.objects.filter(
                detailsignalement__signalement=signalement)
            context["photos"] = photos
        except Signalement.DoesNotExist:
            return


class NouveauSignalementView(LoginRequiredMixin, View):
    login_url = '/connexion/'
    form_class = SignalementForm
    initial = {"date": timezone.now()}

    def get(self, request):
        form = self.form_class(initial=self.initial)
        context = {}
        context["form"] = form
        return render(request, "nouveau_signalement.html", context)

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            try:
                localisation = Localisation()
                localisation.longitude = form.cleaned_data["longitude"]
                localisation.latitude = form.cleaned_data["latitude"]
                localisation.save()
                signalement = Signalement()
                signalement.date = now()
                signalement.description = form.cleaned_data["description"]
                signalement.utilisateur = Utilisateur.objects.get(
                    user=request.user)
                signalement.localisation = localisation
                signalement.save()

                json_data = json.loads(form.cleaned_data["photos_pks"])
                print(str(json_data))
                for photo_pk in json_data["photos_pks"]:
                    detail = DetailSignalement()
                    detail.signalement = signalement
                    detail.photo = Photo.objects.get(pk=photo_pk)
                    detail.save()

                form = self.form_class(initial=self.initial)
                return render(
                    request, "nouveau_signalement.html",
                    {'form': form, 'reussite': True})
            except Exception:
                return render(
                    request, "nouveau_signalement.html",
                    {'form': form, 'erreur': True})
        else:
            render(request, "nouveau_signalement.html", {'form': form})


class MessagesView(LoginRequiredMixin, View):
    login_url = '/connexion/'

    def get(self, request):
        context = {}
        context["entetes"] = ["Date", "Expéditeur", "Sujet"]
        context["messages"] = messages_utilisateur(request.user.email)
        return render(request, "messages.html", context)


class DetailsMessageView(LoginRequiredMixin, View):
    login_url = '/connexion/'

    def get(self, request, message_id):
        context = {}
        message = Message.objects.get(id=message_id)
        context["message"] = message
        return render(request, "details_message.html", context)


class ReponseMessageView(LoginRequiredMixin, View):
    login_url = '/connexion/'
    form_class = MessageForm
    initial = {}

    def get(self, request, message_id):
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
                request, "reponse_message.html", context)


class ProfilView(LoginRequiredMixin, View):
    login_url = '/connexion/'
    form_class = ProfilForm
    initial = {}

    def get(self, request):
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


class TelechargementView(LoginRequiredMixin, View):
    login_url = '/connexion/'

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