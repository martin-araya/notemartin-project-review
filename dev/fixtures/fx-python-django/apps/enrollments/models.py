from django.conf import settings
from django.db import models

from .managers import EnrollmentManager


class Enrollment(models.Model):
    STATUS_PENDING = "pending"
    STATUS_ACTIVE = "active"
    STATUS_CANCELLED = "cancelled"
    STATUS_COMPLETED = "completed"
    STATUS_CHOICES = [
        (STATUS_PENDING, "Pending"),
        (STATUS_ACTIVE, "Active"),
        (STATUS_CANCELLED, "Cancelled"),
        (STATUS_COMPLETED, "Completed"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="enrollments",
    )
    status = models.CharField(max_length=16, choices=STATUS_CHOICES, default=STATUS_PENDING)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Trampa E03: Manager via from_queryset expone .active(), .paid(), .by_user()
    # que NO son metodos estandar de Manager. La skill debe leer managers.py.
    objects = EnrollmentManager()

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"Enrollment#{self.pk}({self.status})"


class EnrollmentItem(models.Model):
    enrollment = models.ForeignKey(
        Enrollment,
        on_delete=models.CASCADE,
        related_name="items",
    )
    sku = models.CharField(max_length=64)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self) -> str:
        return f"{self.sku} x{self.quantity}"