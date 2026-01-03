from rest_framework import serializers
from deals.models import ScanJob, DealResult


class ScanJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScanJob
        fields = "__all__"


class DealResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = DealResult
        fields = "__all__"
