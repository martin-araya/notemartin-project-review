from django.db import models


class PaymentQuerySet(models.QuerySet):
    def completed(self):
        return self.filter(status=Payment.STATUS_COMPLETED)

    def pending(self):
        return self.filter(status=Payment.STATUS_PENDING)

    def for_enrollment(self, enrollment):
        return self.filter(enrollment=enrollment)


PaymentManager = models.Manager.from_queryset(PaymentQuerySet)