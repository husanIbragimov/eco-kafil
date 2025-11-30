from rest_framework import serializers

from apps.weather.models import Weather


class WeatherSerializer(serializers.ModelSerializer):
    region_code = serializers.CharField(source='station.code', read_only=True)
    region_name = serializers.CharField(source='station.name', read_only=True)

    class Meta:
        model = Weather
        fields = (
            "region_code",
            "region_name",
            "humidity",
            "temperature",
            "wind_speed",
            "pressure",
            "precipitation",
            "pm2_5",
            "pm10",
            "fog",
            "aqi",
            "date",
        )
        read_only_fields = ("id", "date")
