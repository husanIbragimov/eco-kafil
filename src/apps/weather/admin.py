from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from apps.weather.resource import WeatherResource
from apps.weather.models import Weather



@admin.register(Weather)
class WeatherAdmin(ImportExportModelAdmin):
    resource_class = WeatherResource
    list_display = (
        'id', 'station', 'temperature', 'humidity', 'wind_speed',
        'pressure', 'precipitation', 'pm2_5', 'pm10', 'fog', 'aqi', 'date',
    )
    list_select_related = ('station',)
