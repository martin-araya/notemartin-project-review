from rest_framework import viewsets

from .models import Certificate
from .serializers import CertificateSerializer


class CertificateViewSet(viewsets.ModelViewSet):
    queryset = Certificate.objects.all()
    serializer_class = CertificateSerializer


class LegacyCertificateViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet legacy NO registrado en urls.py (trampa S01)."""
    queryset = Certificate.objects.all()
    serializer_class = CertificateSerializer