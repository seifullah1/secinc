from rest_framework import serializers
from .models import Incident

class IncidentSerializer(serializers.ModelSerializer):
    reporter_username = serializers.CharField(source="reporter.username", read_only=True)
    assignee_username = serializers.CharField(source="assignee.username", read_only=True)

    class Meta:
        model = Incident
        fields = "__all__"
        read_only_fields = ("created_at", "closed_at", "reporter")
