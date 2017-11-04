"""
    Les routes
"""
from django.conf.urls import url

from sosfrene_client.views import (
    EnregistrementView, DeconnexionView, ConnexionView,
    SignalementsView, DetailsSignalementView, NouveauSignalementView,
    MessagesView, DetailsMessageView, ReponseMessageView, ProfilView,
    TelechargementView, AccueilView, CarteView, FreneView, AgrileView,
    SymptomesView, SpecimensCarteView, NotificationsView,
    ArchiverNotificationView
)

urlpatterns = [
    url(r'^$', AccueilView.as_view(), name="accueil"),
    url(r'^carte/$', CarteView.as_view(), name="carte"),
    url(r'^specimens-carte/$', SpecimensCarteView.as_view(),
        name="specimens-carte"),
    url(r'^frene/$', FreneView.as_view(), name="frene"),
    url(r'^agrile/$', AgrileView.as_view(), name="agrile"),
    url(r'^symptomes/$', SymptomesView.as_view(), name="symptomes"),
    url(r'^enregistrement/$', EnregistrementView.as_view(),
        name="enregistrement"),
    url(r'^connexion/$', ConnexionView.as_view(), name="connexion"),
    url(r'^deconnexion/$', DeconnexionView.as_view(), name="deconnexion"),
    url(r'^notifications/$', NotificationsView.as_view(),
        name="notifications"),
    url(r'^archiver-notifications/$',
        ArchiverNotificationView.as_view(), name="archiver_notification"),
    url(r'^signalements/$', SignalementsView.as_view(), name="signalements"),
    url(r'^signalements/nouveau/$', NouveauSignalementView.as_view(),
        name="nouveau_signalement"),
    url(r'^signalements/(?P<signalement_id>[0-9]+)/$',
        DetailsSignalementView.as_view(), name="detailssignalement"),
    url(r'^messages/$', MessagesView.as_view(), name="messages"),
    url(r'^messages/(?P<message_id>[0-9]+)/$',
        DetailsMessageView.as_view(), name="details_message"),
    url(r'^messages/(?P<message_id>[0-9]+)/reponse/$',
        ReponseMessageView.as_view(), name="reponse"),
    url(r'^profil/$', ProfilView.as_view(), name="profil"),
    url(r'^telechargement/$', TelechargementView.as_view(),
        name="telechargement")
]
