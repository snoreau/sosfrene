"""
    Les routes
"""
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    url(r'^admin/', include("sosfrene_admin.urls",
                            namespace="admin")),
    url(r'^', include("sosfrene_client.urls",
                       namespace="client")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
