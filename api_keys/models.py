from django.db import models
from django.utils import timezone


class APIKey(models.Model):
    """Model to store API keys with usage tracking for rotation."""

    name = models.CharField(
        max_length=255,
        help_text="Descriptive name for the API key",
        blank=True,
        null=True,
    )
    key = models.CharField(
        max_length=500, unique=True, help_text="The actual API key value"
    )
    usage_count = models.IntegerField(
        default=0,
        help_text="Number of times this key has been used",
        null=True,
        blank=True,
    )
    is_active = models.BooleanField(
        default=True, help_text="Whether this key should be included in rotation"
    )
    last_used_at = models.DateTimeField(
        null=True, blank=True, help_text="Timestamp of last use"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["last_used_at", "created_at"]
        verbose_name = "API Key"
        verbose_name_plural = "API Keys"

    def __str__(self):
        return f"{self.name} ({'Active' if self.is_active else 'Inactive'})"

    @classmethod
    def get_next_key(cls):
        """
        Get the next API key to use based on round-robin rotation.
        Returns the active key that was used longest ago (or never used).
        Updates the usage_count and last_used_at timestamp.
        """
        # Get the least recently used active API key
        api_key = (
            cls.objects.filter(is_active=True)
            .order_by("last_used_at", "created_at")
            .first()
        )

        if not api_key:
            return None

        # Update usage statistics
        api_key.usage_count += 1
        api_key.last_used_at = timezone.now()
        api_key.save(update_fields=["usage_count", "last_used_at"])

        return api_key
