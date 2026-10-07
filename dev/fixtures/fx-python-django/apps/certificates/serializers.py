from rest_framework import serializers

from .models import Certificate


class CertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certificate
        fields = ["id", "enrollment", "serial", "status", "issued_at", "pdf_url"]
        read_only_fields = ["id", "serial", "issued_at", "pdf_url"]