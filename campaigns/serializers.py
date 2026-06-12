from rest_framework import serializers

from .models import Campaign


class CampaignSerializer(serializers.ModelSerializer):
    status = serializers.CharField(read_only=True)

    class Meta:
        model = Campaign
        fields = ["id", "name", "budget", "spend", "status", "created_at"]
        read_only_fields = ["id", "status", "created_at"]
