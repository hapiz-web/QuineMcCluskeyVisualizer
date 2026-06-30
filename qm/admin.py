from django.contrib import admin
from .models import CalculationHistory


@admin.register(CalculationHistory)
class CalculationHistoryAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "variable_count",
        "simplified_expression",
        "execution_time",
        "created_at",
    )

    search_fields = (
        "simplified_expression",
    )

    list_filter = (
        "created_at",
    )