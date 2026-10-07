from django.db import models


class Certificate(models.Model):
    STATUS_DRAFT = "draft"
    STATUS_ISSUED = "issued"
    STATUS_REVOKED = "revoked"
    STATUS_CHOICES = [
        (STATUS_DRAFT, "Draft"),
        (STATUS_ISSUED, "Issued"),
        (STATUS_REVOKED, "Revoked"),
    ]

    enrollment = models.OneToOneField(
        "enrollments.Enrollment",
        on_delete=models.CASCADE,
        related_name="certificate",
    )
    serial = models.CharField(max_length=32, unique=True)
    status = models.CharField(max_length=16, choices=STATUS_CHOICES, default=STATUS_DRAFT)
    issued_at = models.DateTimeField(null=True, blank=True)
    pdf_url = models.URLField(blank=True)

    objects = models.Manager()

    class Meta:
        ordering = ["-issued_at"]

    def __str__(self) -> str:
        return f"Certificate#{self.serial}({self.status})"