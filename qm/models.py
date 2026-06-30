from django.db import models


class CalculationHistory(models.Model):
    variable_count = models.PositiveIntegerField()

    minterms = models.TextField()

    dont_cares = models.TextField(
        blank=True,
        default=""
    )

    simplified_expression = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    execution_time = models.FloatField(
        default=0
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Calculation {self.id}"