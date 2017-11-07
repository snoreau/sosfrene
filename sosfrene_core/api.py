import json
from django.utils.timezone import now
from django.core.mail import send_mail

from sosfrene_core.models import (
    Utilisateur, Signalement, Message, DetailSignalement, Photo,
    Activite, Notification, Specimen, Localisation, Signalement
)
from sosfrene_core.constants import ETATS_SPECIMEN


def courriel_existe(courriel):
    utilisateurs = Utilisateur.objects.filter(user__email=courriel)
    total = len(list(utilisateurs))
    if total > 0:
        return True
    else:
        return False

def signalements_utilisateur(courriel):
    try:
        utilisateur = Utilisateur.objects.get(user__email=courriel)
        return list(Signalement.objects.filter(utilisateur=utilisateur)\
            .order_by("-date"))
    except Utilisateur.DoesNotExist:
        return None

def messages_utilisateur(courriel):
    try:
        utilisateur = Utilisateur.objects.get(user__email=courriel)
        return list(
            Message.objects.filter(receveur=utilisateur).order_by('-date'))
    except Utilisateur.DoesNotExist:
        return None

def creer_activite(description, specimen):
    activite = Activite(date=now(), description=description, specimen=specimen)
    activite.save()
    try:
        signalement = Signalement.objects.get(specimen=specimen)
        notification = Notification.objects.create(
            utilisateur=signalement.utilisateur, date=now(),
            description="Des nouvelles concernant le signalement #"
            + str(signalement.id) + "\n\n" + description)
        notification.save()
        if signalement.utilisateur.notifications:
            envoyer_courriel(signalement.utilisateur.user.email,
                             notification.description,
                             "Notification de S.O.S Frêne")
    except Signalement.DoesNotExist:
        return

def notifications_utilisateur(courriel):
    try:
        utilisateur = Utilisateur.objects.get(user__email=courriel)
        notifications = Notification.objects.filter(
            utilisateur=utilisateur, archive=False)\
                .order_by("-date")
        return notifications
    except Utilisateur.DoesNotExist:
        return None

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

def envoyer_courriel(adresse, message, sujet):
    send_mail(sujet, message, "sosfrene@gmail.com",
              [adresse], fail_silently=False)

def envoyer_message(expediteur, receveur, sujet, message):
    msg = Message.objects.create(date=now(), receveur=receveur,
                                 expediteur=expediteur, sujet=sujet,
                                 contenu=message)
    msg.save()
    notification = Notification.objects.create(
        utilisateur=receveur, date=now(),
        description="Nouveau message\nExpéditeur: {0}.\n"
                    "Sujet: {1}\nContenu: \n\n{2}"\
                    .format(expediteur.user.get_full_name(), sujet, message))
    notification.save()
    if receveur.notifications:
        envoyer_courriel(receveur.user.email, notification.description,
                         "Notification de S.O.S Frêne")

def ajouter_specimen(etat, latitude, longitude):
    if etat not in ETATS_SPECIMEN:
        raise SosfreneErreur("L'état spécifié n'existe pas.")
    specimen = Specimen()
    specimen.etat = ETATS_SPECIMEN[int(etat)]
    localisation = Localisation()
    localisation.latitude = latitude
    localisation.longitude = longitude
    localisation.save()
    specimen.localisation = localisation
    specimen.save()
    return specimen

def creer_signalement(latitude, longitude, description, user, photos):
    localisation = Localisation()
    localisation.longitude = longitude
    localisation.latitude = latitude
    localisation.save()
    signalement = Signalement()
    signalement.date = now()
    signalement.description = description
    signalement.utilisateur = Utilisateur.objects.get(user=user)
    signalement.localisation = localisation
    signalement.save()

    json_data = json.loads(photos)
    for photo_pk in json_data["photos_pks"]:
        detail = DetailSignalement()
        detail.signalement = signalement
        detail.photo = Photo.objects.get(pk=photo_pk)
        detail.save()

    return signalement

class SosfreneErreur(Exception):
    pass
