from django.contrib import admin

from .models import Enrollment, EnrollmentItem


class EnrollmentItemInline(admin.TabularInline):
    model = EnrollmentItem
    extra = 0


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "status", "total", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("user__username",)
    inlines = [EnrollmentItemInline]