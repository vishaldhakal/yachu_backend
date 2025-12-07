from django.db import models


# Create your models here.
class AIData(models.Model):
    ai_json_data = models.JSONField()

    def __str__(self):
        return str(self.id)
