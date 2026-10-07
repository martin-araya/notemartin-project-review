from rest_framework import serializers

from .models import Enrollment, EnrollmentItem


class EnrollmentItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnrollmentItem
        fields = ["id", "sku", "quantity", "unit_price"]


class EnrollmentSerializer(serializers.ModelSerializer):
    items = EnrollmentItemSerializer(many=True, read_only=True)

    class Meta:
        model = Enrollment
        fields = ["id", "user", "status", "total", "created_at", "updated_at", "items"]
        read_only_fields = ["id", "created_at", "updated_at", "total"]