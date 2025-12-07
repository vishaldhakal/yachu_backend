from django.db import models


# Create your models here.
class AIData(models.Model):
    ai_json_data = models.JSONField()
    extracted_json_data = models.JSONField(null=True, blank=True)
    conversation_json_data = models.JSONField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)
