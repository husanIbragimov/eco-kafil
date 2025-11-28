from django.db import models

from apps.common.choices.map_type import MapType


class Map(models.Model):
    map_type = models.SmallIntegerField(default=0, choices=MapType.choices)
    data = models.FileField(upload_to="maps/")

    def __str__(self):
        return f"{self.map_type}"
