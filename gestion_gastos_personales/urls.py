"""
URL configuration for gestion_gastos_personales project.

El enrutamiento de la app MTV vive en gastos.urls.
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("gastos.urls")),
    # Rutas de auth restantes (password reset, etc.)
    path("accounts/", include("django.contrib.auth.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
