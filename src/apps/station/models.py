from django.db import models


class Station(models.Model):
    title = models.JSONField(default=dict)
    name = models.CharField(max_length=255)
    code = models.BigIntegerField(unique=True, null=True)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name="children")

    def __str__(self):
        if not self.parent_id:
            return f"{self.name} ({self.code})"
        return f"{self.parent.name} / {self.name} ({self.code})"
