from rest_framework import serializers

from apps.weather.models import Weather


class WeatherSerializer(serializers.ModelSerializer):
    region_code = serializers.CharField(source='station.code', read_only=True)
    region_name = serializers.CharField(source='station.name', read_only=True)
    pollutant = serializers.SerializerMethodField()

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
            "pollutant",
        )
        read_only_fields = ("id", "date")

    def get_pollutant(self, obj: Weather):
        if obj.aqi > 0:
            if obj.aqi < 50:
                return "good"
            elif 50 <= obj.aqi < 100:
                return "moderate"
            elif 100 <= obj.aqi < 150:
                return "unhealthy for sensitive groups"
            elif 150 <= obj.aqi < 200:
                return "unhealthy"
            elif 200 <= obj.aqi < 300:
                return "very unhealthy"
            else:
                return "hazardous"
        return "no data"
