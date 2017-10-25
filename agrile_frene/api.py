from .models import Utilisateur, Signalement, Message

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
        return list(Signalement.objects.filter(utilisateur=utilisateur))

def messages_utilisateur(courriel):
    utilisateur = Utilisateur.objects.get(user__email=courriel)
    if utilisateur is not None:
        return list(
            Message.objects.filter(receveur=utilisateur).order_by('-date'))

def specimens():
    specimens = Specimen.objects.all()
