import uuid
from django.db import models


class ScanJob(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    status = models.CharField(max_length=50)
    started_at = models.DateTimeField()
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class DealResult(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    scan_job = models.ForeignKey(ScanJob, on_delete=models.CASCADE)

    deal_id = models.CharField(max_length=100, null=True, blank=True)    # ✅ NOT hubspot_deal_id
    deal_name = models.CharField(max_length=255)
    pipeline = models.CharField(max_length=100)
    stage = models.CharField(max_length=100)          # ✅ NOT deal_stage
    amount = models.DecimalField(max_digits=12, decimal_places=2, null=True)
    close_date = models.DateTimeField(null=True)

    created_at = models.DateTimeField(auto_now_add=True)


