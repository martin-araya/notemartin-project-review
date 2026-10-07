"""URL configuration for fxdjango project.

Trampa E02: las rutas de la API se incluyen via routers de DRF (DefaultRouter),
no via path() literales. La skill debe saltar a apps/<app>/urls.py para
encontrar el basename y el queryset que genera las rutas.
"""
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/enrollments/", include("apps.enrollments.urls")),
    path("api/payments/", include("apps.payments.urls")),
    path("api/certificates/", include("apps.certificates.urls")),
    path("admin/audit/", include("apps.audit.urls_admin")),
]