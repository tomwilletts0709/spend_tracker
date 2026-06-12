from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models


class Campaign(models.Model):
    class Status(models.TextChoices):
        OK = "ok", "On track"
        WARNING = "warning", "At risk"
        OVERSPENT = "overspent", "Overspent"

    WARNING_THRESHOLD = Decimal("0.90")

    name = models.CharField(max_length=200)
    budget = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))],
    )
    spend = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00"),
        validators=[MinValueValidator(Decimal("0.00"))],
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    @property
    def status(self):
        if self.spend > self.budget:
            return self.Status.OVERSPENT
        if self.spend >= self.budget * self.WARNING_THRESHOLD:
            return self.Status.WARNING
        return self.Status.OK

    def __str__(self):
        return self.name
