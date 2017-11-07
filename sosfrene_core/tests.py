from django.test import TestCase

from sosfrene_core.constants import ATTEINT, ETATS_SPECIMEN
from sosfrene_core.models import Utilisateur, Specimen, Activite
from sosfrene_core.api import (
    courriel_existe, signalements_utilisateur, messages_utilisateur,
    envoyer_message, notifications_utilisateur, ajouter_specimen,
    SosfreneErreur, specimens_carte, creer_activite, creer_signalement
)


class CoreApiTestCase(TestCase):
    fixtures = ["basic"]

    def test_courriel_existe(self):
        existe = courriel_existe("blabla@bla.com")
        self.assertFalse(existe)
        existe = courriel_existe("mtlbidon@gmail.com")
        self.assertTrue(existe)
        existe = courriel_existe(123)
        self.assertFalse(existe)

    def test_signalements_utilisateur(self):
        signalements = signalements_utilisateur("blabla@blab.com")
        self.assertIsNone(signalements)
        signalements = signalements_utilisateur(123)
        self.assertIsNone(signalements)
        signalements = signalements_utilisateur("mtlbidon@gmail.com")
        self.assertEqual(len(signalements), 1)

    def test_messages_utilisateur(self):
        messages = messages_utilisateur("blabla@blab.com")
        self.assertIsNone(messages)
        messages = messages_utilisateur("mtlbidon@gmail.com")
        self.assertEqual(len(messages), 0)

        expediteur = Utilisateur.objects.get(user__email="sosfrene@gmail.com")
        receveur = Utilisateur.objects.get(user__email="mtlbidon@gmail.com")
        envoyer_message(expediteur, receveur, "test", "Un test.")
        messages = messages_utilisateur("mtlbidon@gmail.com")
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].contenu, "Un test.")
        self.assertEqual(messages[0].sujet, "test")
        self.assertEqual(messages[0].expediteur, expediteur)

    def test_notifications_utilisateur(self):
        notifications = notifications_utilisateur("blabla@blab.com")
        self.assertIsNone(notifications)

        expediteur = Utilisateur.objects.get(user__email="sosfrene@gmail.com")
        receveur = Utilisateur.objects.get(user__email="mtlbidon@gmail.com")
        envoyer_message(expediteur, receveur, "test", "Un test.")
        notifications = notifications_utilisateur("mtlbidon@gmail.com")
        self.assertEqual(len(notifications), 1)

    def test_ajouter_specimen(self):
        specimen = ajouter_specimen(ATTEINT, 45.3424323, -73.3333)
        self.assertIsNotNone(specimen)
        self.assertEqual(specimen.etat, ETATS_SPECIMEN[ATTEINT])
        self.assertEqual(specimen.localisation.latitude, 45.3424323)

        with self.assertRaises(SosfreneErreur):
            ajouter_specimen(-1, 45.3424323, -73.3333)

    def test_specimens_carte(self):
        specimens = specimens_carte()
        self.assertEqual(len(specimens), 3)
        ajouter_specimen(ATTEINT, 45.3424323, -73.3333)
        ajouter_specimen(ATTEINT, 43.3424323, -72.3333)
        specimens = specimens_carte()
        self.assertEqual(len(specimens), 5)
        self.assertEqual(specimens[4]["latitude"], 43.3424323)
        self.assertEqual(specimens[4]["etat"], ETATS_SPECIMEN[ATTEINT])

    def test_creer_activite(self):
        specimen = Specimen.objects.get(id=9)
        creer_activite("Une activité intéressante.", specimen)
        activite = Activite.objects.get(
            description="Une activité intéressante.")
        self.assertIsNotNone(activite)

    def test_creer_signalement(self):
        utilisateur = Utilisateur.objects.get(user__email="mtlbidon@gmail.com")
        signalement = creer_signalement(
            45.3424323, -73.3333, "Un arbre qui semble atteint...",
            utilisateur.user, '{"photos_pks": [8]}')
        self.assertIsNotNone(signalement)
