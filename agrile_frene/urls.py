"""
    Les routes
"""
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.AccueilView.as_view(), name="accueil"),
    url(r'^enregistrement/$', views.EnregistrementView.as_view(),
        name="enregistrement"),
    url(r'^connexion/$', views.ConnexionView.as_view(),
        name="connexion"),
    url(r'^deconnexion/$', views.DeconnexionView.as_view(),
        name="deconnexion"),
    url(r'^signalements/$', views.SignalementsView.as_view(),
        name="signalements"),
    url(r'^signalements/nouveau/$', views.NouveauSignalementView.as_view(),
        name="nouveau_signalement"),
    url(r'^messages/$', views.MessagesView.as_view(),
        name="messages"),
    url(r'^profile/$', views.ProfileView.as_view(),
        name="profile")
]
