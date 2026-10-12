from django.db import models


class AQI(models.Model):
    aqi = models.CharField(max_length=255)
    dateTime = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ["-dateTime"]
        indexes = [
            models.Index(fields=["-dateTime"]),
        ]
        verbose_name = "AQI"
        verbose_name_plural = "AQIs"

    def __str__(self):
        return f"{self.aqi} - {self.dateTime}"
