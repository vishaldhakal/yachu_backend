from django.db import models


class PriceGuess(models.Model):
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    yachu_facewash_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0
    )
    yachu_bodylotion_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0
    )
    yachu_brightening_cream_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Price Guess"
        verbose_name_plural = "Price Guesses"

    def __str__(self):
        return f"{self.name} - {self.phone_number}"
