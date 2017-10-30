from django.utils.timezone import now

from sosfrene_core.models import (
    Utilisateur, Signalement, Message,
    Activite, Notification, Specimen
)

def courriel_existe(courriel):
    utilisateurs = Utilisateur.objects.filter(user__email=courriel)
    total = len(list(utilisateurs))
    if total > 0:
        return True
    else:
        return False

def signalements_utilisateur(courriel):
    utilisateur = Utilisateur.objects.get(user__email=courriel)
    if utilisateur is not None:
        return list(Signalement.objects.filter(utilisateur=utilisateur)\
            .order_by("-date"))

def messages_utilisateur(courriel):
    utilisateur = Utilisateur.objects.get(user__email=courriel)
    if utilisateur is not None:
        return list(
            Message.objects.filter(receveur=utilisateur).order_by('-date'))

def creer_activite(type, description, specimen):
    activite = Activite(now(), type, description, specimen)
    activite.save()
    signalement = specimen.signalement.get()
    if signalement:
        notification = Notification(activite)
        notification.save()

def notifications_utilisateur(courriel):
    utilisateur = Utilisateur.objects.get(user__email=courriel)
    if utilisateur is not None:
        notifications = Notification.objects.filter(
            activite__specimen__signalement__utilisateur=utilisateur)

def specimens_carte():
    nouvelle_liste = []
    liste_specimens = list(Specimen.objects.all())
    for specimen in liste_specimens:
        nouveau_dict = {}
        nouveau_dict["id"] = specimen.id
        nouveau_dict["etat"] = specimen.etat
        nouveau_dict["latitude"] = specimen.localisation.latitude
        nouveau_dict["longitude"] = specimen.localisation.longitude
        nouvelle_liste.append(nouveau_dict)
    return nouvelle_liste
