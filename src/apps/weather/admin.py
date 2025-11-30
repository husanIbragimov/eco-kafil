from django.contrib import admin

from apps.weather.models import Weather


@admin.register(Weather)
class WeatherAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'station', 'temperature', 'humidity', 'wind_speed',
        'pressure', 'precipitation', 'pm2_5', 'pm10', 'fog', 'aqi',
    )
    list_select_related = ('station',)
