from django.db import models


class CertificateQuerySet(models.QuerySet):
    def issued(self):
        return self.filter(status=Certificate.STATUS_ISSUED)

    def for_enrollment(self, enrollment):
        return self.filter(enrollment=enrollment)


CertificateManager = models.Manager.from_queryset(CertificateQuerySet)