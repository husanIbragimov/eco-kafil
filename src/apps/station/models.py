from django.db import models


class Station(models.Model):
    title = models.JSONField(default=dict)
    name = models.CharField(max_length=255)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name="children")

    def __str__(self):
        return f"{self.name}"
