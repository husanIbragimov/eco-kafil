from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Feedback(models.Model):
    text = models.TextField()
    phone = models.CharField(max_length=15)
    rate = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name="children")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.phone:
            return f"{self.phone}"
        return f"{self.id}"
