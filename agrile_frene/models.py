""" Définit les modèles du système """

from django.db import models
from django.contrib.auth.models import User


class Utilisateur(models.Model):
    """ Définit un utilisateur du système SOS Frêne """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    notifications = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)

class Message(models.Model):
    """ Définit un message envoyé par un utilisateur """
    date = models.DateTimeField()
    expediteur = models.ForeignKey(Utilisateur, related_name="+")
    receveur = models.ForeignKey(Utilisateur, related_name="+")
    contenu = models.CharField(max_length=1000)
    sujet = models.CharField(max_length=80, default=None)

class Localisation(models.Model):
    """ Définit un emplacement géographique """
    latitude = models.FloatField()
    longitude = models.FloatField()

class Specimen(models.Model):
    """ Définit un arbre répertorié """
    etat = models.CharField(max_length=50)
    localisation = models.ForeignKey(Localisation)

class Activite(models.Model):
    """ Définit une activité concernant un spécimen
    et le personnel de la ville """
    date = models.DateTimeField()
    type = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    specimen = models.ForeignKey(Specimen, related_name="activites")

class Signalement(models.Model):
    """ Définit les Signalements de spécimen faites
        par un utilisateur
    """
    date = models.DateTimeField()
    description = models.CharField(max_length=500)
    utilisateur = models.ForeignKey(Utilisateur)
    localisation = models.ForeignKey(Localisation)
    accepte = models.BooleanField(default=False)
    specimen = models.ForeignKey(
        Specimen, null=True, related_name="signalement")

class Photo(models.Model):
    """ Définit une photo soumise par un utilisateur """
    description = models.CharField(max_length=500)
    source = models.ImageField(upload_to='uploads/')

class DetailSignalement(models.Model):
    """ Définit chaque photo soumise par Signalement """
    signalement = models.ForeignKey(Signalement)
    photo = models.ForeignKey(Photo)

class Notification(models.Model):
    """ Définit les alertes crées suite à une activité """
    date = models.DateTimeField()
    activite = models.ForeignKey(Activite)
    specimen = models.ForeignKey(Specimen)
