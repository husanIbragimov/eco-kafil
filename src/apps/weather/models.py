from django.db import models


class Weather(models.Model):
    temperature = models.FloatField(default=0)
    wind_speed = models.FloatField(default=0)
    humidity = models.FloatField(default=0)
    pressure = models.FloatField(default=0)
    description = models.CharField(max_length=255, blank=True, null=True)

