from django.db import models


class MapType(models.IntegerChoices):
    REGIONAL = 0, "REGIONAL"
    DISTRICT = 1, "DISTRICT"
