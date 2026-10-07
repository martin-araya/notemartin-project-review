from django.contrib import admin

from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("id", "enrollment", "amount", "status", "provider", "created_at")
    list_filter = ("status", "provider")
    search_fields = ("enrollment__id",)