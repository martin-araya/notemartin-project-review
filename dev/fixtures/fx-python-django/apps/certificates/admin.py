from django.contrib import admin

from .models import Certificate


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ("id", "serial", "status", "issued_at")
    list_filter = ("status",)
    search_fields = ("serial",)