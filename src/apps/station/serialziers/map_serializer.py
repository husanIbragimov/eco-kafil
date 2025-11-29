from rest_framework import serializers

from apps.station.models import Station

class StationSerializer(serializers.ModelSerializer):
    data = serializers.ListField(child=serializers.JSONField())

    class Meta:
        model = Station
        fields = "__all__"
