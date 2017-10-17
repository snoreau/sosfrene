import logging
from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone

from .forms import EnregistrementForm, ConnexionForm, SignalementForm
from .models import Utilisateur
from .api import signalements_utilisateur

logger = logging.getLogger(__name__)

class AccueilView(View):

    def get(self, request):
        print(request.user)
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
            return render(
                request, "enregistrement.html", {'form': form})

        return render(request, "enregistrement.html",
                      {'form': form, "reussite": True})


class ConnexionView(View):
    form_class = ConnexionForm
    initial = {}

    def get(self, request):
        if request.user.is_authenticated():
            return redirect("accueil")

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
                              {'form': form, "erreur": True})

        return render(request, "connexion.html", {'form': form})


class DeconnexionView(View):
    def get(self, request):
        logout(request)
        return redirect("accueil")


class SignalementsView(LoginRequiredMixin, View):

    def get(self, request):
        context = {}
        context["signalements"] = signalements_utilisateur(request.user)
        return render(request, "signalements.html", context)


class NouveauSignalementView(LoginRequiredMixin, View):
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
            pass

        return render(request, "nouveau_signalement.html", {'form': form})


class MessagesView(View):

    def get(self, request):
        pass


class ProfileView(View):

    def get(self, request):
        pass
