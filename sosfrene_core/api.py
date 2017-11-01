from django.utils.timezone import now
from django.core.mail import send_mail

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
            Message.objects.filter(receveur=utilisateur).order_by('date'))

def creer_activite(description, specimen):
    activite = Activite(date=now(), description=description, specimen=specimen)
    activite.save()
    signalement = specimen.signalement.get()
    if signalement is not None:
        notification = Notification.objects.create(
            utilisateur=signalement.utilisateur, date=now(),
            description="Le spécimen associé au signalement que "
            "vous avez fait a une nouvelle activité:\n\n" + description)
        notification.save()
        if signalement.utilisateur.notifications:
            envoyer_courriel(signalement.utilisateur.user.email,
                             notification.description,
                             "Notification de S.O.S Frêne")

def notifications_utilisateur(courriel):
    utilisateur = Utilisateur.objects.get(user__email=courriel)
    if utilisateur is not None:
        notifications = Notification.objects.filter(
            utilisateur=utilisateur)\
                .order_by("-date")
        return notifications

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
        description="Nouveau message de la part de: {0}.\n"
                    "Sujet: {1}\nContenu: \n\n{2}"\
                    .format(expediteur.user.get_full_name(), sujet, message))
    notification.save()
    if receveur.notifications:
        envoyer_courriel(receveur.user.email, notification.description,
                         "Notification de S.O.S Frêne")
