"""
    Les routes
"""
from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
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
    url(r'^signalements/(?P<signalement_id>[0-9]+)/$',
        views.DetailsSignalementView.as_view(),
        name="detailssignalement"),
    url(r'^messages/$', views.MessagesView.as_view(),
        name="messages"),
    url(r'^profil/$', views.ProfilView.as_view(),
        name="profil"),
    url(r'^telechargement/$', views.TelechargementView.as_view(),
        name="telechargement")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
