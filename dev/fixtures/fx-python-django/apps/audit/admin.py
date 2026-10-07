"""Admin with custom actions for the audit app (trampa E05 + trampa P03).

Las acciones export_csv y mark_reviewed estan registradas via @admin.action
pero NO tienen una ruta publica: solo son accesibles desde el shell de
Django admin y requieren permisos de staff (no verifican un permiso
adicional como would_django_staff_member_required).
"""
import csv

from django.contrib import admin
from django.http import HttpResponse

from .models import AuditLog


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ("id", "actor", "action", "target", "level", "reviewed", "created_at")
    list_filter = ("level", "reviewed", "created_at")
    search_fields = ("action", "target")
    actions = ["export_csv", "mark_reviewed"]

    @admin.action(description="Export selected audit logs as CSV")
    def export_csv(self, request, queryset):
        """Exporta los logs seleccionados a CSV.

        Trampa P03: NO verifica un permiso extra sobre el que ya exige
        has_module_perms para acceder al admin. Cualquier usuario con
        acceso al admin puede exportar.
        """
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="audit_logs.csv"'
        writer = csv.writer(response)
        writer.writerow(["id", "actor", "action", "target", "level", "reviewed", "created_at"])
        for log in queryset:
            writer.writerow([
                log.id,
                log.actor.username if log.actor else "",
                log.action,
                log.target,
                log.level,
                log.reviewed,
                log.created_at.isoformat() if log.created_at else "",
            ])
        return response

    @admin.action(description="Mark selected logs as reviewed")
    def mark_reviewed(self, request, queryset):
        """Marca los logs seleccionados como revisados."""
        queryset.update(reviewed=True)
        self.message_user(request, f"{queryset.count()} logs marcados como revisados.")