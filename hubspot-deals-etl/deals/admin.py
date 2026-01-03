from django.contrib import admin
from .models import ScanJob, DealResult


@admin.register(ScanJob)
class ScanJobAdmin(admin.ModelAdmin):
    list_display = ("id", "status", "started_at", "completed_at", "created_at")
    readonly_fields = ("id", "created_at")


@admin.register(DealResult)
class DealResultAdmin(admin.ModelAdmin):
    list_display = (
        "deal_id",      # ✅ correct field
        "deal_name",
        "stage",        # ✅ correct field
        "pipeline",
        "amount",
        "created_at",
    )
    list_filter = ("pipeline", "stage")
    search_fields = ("deal_id", "deal_name")
