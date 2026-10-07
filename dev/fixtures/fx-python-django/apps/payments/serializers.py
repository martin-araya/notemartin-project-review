from rest_framework import serializers

from .models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ["id", "enrollment", "amount", "status", "provider", "created_at", "paid_at"]
        read_only_fields = ["id", "created_at", "paid_at"]