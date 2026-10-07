from django.urls import path

from .views import export_audit_csv

urlpatterns = [
    path("export/", export_audit_csv, name="export-audit-csv"),
]