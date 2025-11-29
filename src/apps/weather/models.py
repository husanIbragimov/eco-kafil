from django.db import models

from apps.station.models import Station


class Weather(models.Model):
    humidity = models.FloatField(default=0)
    temperature = models.FloatField(default=0)
    wind_speed = models.FloatField(default=0)
    pressure = models.FloatField(default=0)
    precipitation = models.FloatField(default=0)
    pm2_5 = models.FloatField(default=0)
    pm10 = models.FloatField(default=0)
    fog = models.SmallIntegerField(default=0)
    aqi = models.FloatField(default=0)
    station_name = models.CharField(max_length=255, blank=True, null=True)
    station = models.ForeignKey(Station, on_delete=models.CASCADE, related_name="weather", blank=True, null=True)

    def __str__(self):
        return f"{self.id}"
