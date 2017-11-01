"""
    Les routes
"""
from django.conf.urls import url

from sosfrene_admin.views import (
    TableauBordView, ConnexionView, DeconnexionView, SignalementsView,
    DetailsMessageView, DetailsSignalementView, TraiterSignalementView,
    SpecimensView, NouveauSpecimenView, MessagesView,
    ReponseMessageView, DetailsSpecimenView,
    SupprimerSpecimenView, NouvelleActiviteView, AdministrateursView
)


urlpatterns = [
    url(r'^$', TableauBordView.as_view(),
        name="tableau_bord"),
    url(r'^connexion/$', ConnexionView.as_view(),
        name="connexion"),
    url(r'^deconnexion/$', DeconnexionView.as_view(),
        name="deconnexion"),
    url(r'^signalements/$', SignalementsView.as_view(),
        name="signalements"),
    url(r'^signalements/(?P<signalement_id>[0-9]+)/$',
        DetailsSignalementView.as_view(),
        name="detailssignalement"),
    url(r'^signalements/(?P<signalement_id>[0-9]+)/traitement/$',
        TraiterSignalementView.as_view(),
        name="traiter_signalement"),
    url(r'^specimens/$', SpecimensView.as_view(),
        name="specimens"),
    url(r'^specimens/nouveau/$', NouveauSpecimenView.as_view(),
        name="nouveau_specimen"),
    url(r'^specimens/(?P<specimen_id>[0-9]+)/$',
        DetailsSpecimenView.as_view(), name="details_specimen"),
    url(r'^specimens/supprimer/(?P<specimen_id>[0-9]+)/$',
        SupprimerSpecimenView.as_view(), name="supprimer_specimen"),
    url(r'^messages/$', MessagesView.as_view(),
        name="messages"),
    url(r'^messages/(?P<message_id>[0-9]+)/$',
        DetailsMessageView.as_view(), name="details_message"),
    url(r'^messages/(?P<message_id>[0-9]+)/reponse/$',
        ReponseMessageView.as_view(), name="reponse"),
    url(r'^administrateurs/$', AdministrateursView.as_view(),
        name="gestion"),
    url(r'^specimens/(?P<specimen_id>[0-9]+)/nouvelle-activite/$', NouvelleActiviteView.as_view(),
        name="activite")
]
