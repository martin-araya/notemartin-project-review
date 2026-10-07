"""Custom Manager + QuerySet for Enrollment (trampa E03).

La skill debe notar que EnrollmentQuerySet expone active() y paid(),
y que EnrollmentManager (built via from_queryset) lo expone via .active().
"""
from django.db import models


class EnrollmentQuerySet(models.QuerySet):
    def active(self):
        return self.filter(status=Enrollment.STATUS_ACTIVE)

    def paid(self):
        return self.filter(status__in=[Enrollment.STATUS_COMPLETED, Enrollment.STATUS_ACTIVE])

    def by_user(self, user):
        return self.filter(user=user)


EnrollmentManager = models.Manager.from_queryset(EnrollmentQuerySet)