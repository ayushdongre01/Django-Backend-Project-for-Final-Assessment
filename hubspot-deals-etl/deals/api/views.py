import uuid
from datetime import datetime
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from deals.models import ScanJob, DealResult
from deals.api.serializers import ScanJobSerializer, DealResultSerializer
from deals.services.hubspot_client import fetch_deals

@method_decorator(csrf_exempt, name="dispatch")

class StartScanAPIView(APIView):
    def post(self, request):
        scan_job = ScanJob.objects.create(
            id=str(uuid.uuid4()),
            status="RUNNING",
            started_at=datetime.utcnow(),
        )

        after = None
        total = 0

        while True:
            data = fetch_deals(after=after)
            deals = data.get("results", [])

            for d in deals:
                props = d.get("properties", {})

                DealResult.objects.create(
                    scan_job=scan_job,
                    deal_id=d.get("id"),
                    deal_name=props.get("dealname"),
                    stage=props.get("dealstage"),
                    pipeline=props.get("pipeline"),
                    amount=props.get("amount"),
                )

                total += 1

            paging = data.get("paging")
            if not paging or "next" not in paging:
                break

            after = paging["next"]["after"]

        scan_job.status = "COMPLETED"
        scan_job.completed_at = datetime.utcnow()
        scan_job.save()

        return Response(
            {
                "scan_job_id": scan_job.id,
                "deals_fetched": total,
                "status": scan_job.status,
            },
            status=status.HTTP_201_CREATED,
        )
class ScanStatusAPIView(APIView):
    def get(self, request, scan_job_id):
        try:
            scan_job = ScanJob.objects.get(id=scan_job_id)
        except ScanJob.DoesNotExist:
            return Response(
                {"error": "Scan job not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = ScanJobSerializer(scan_job)
        return Response(serializer.data)

class ScanResultsAPIView(APIView):
    def get(self, request, scan_job_id):
        results = DealResult.objects.filter(scan_job_id=scan_job_id)
        serializer = DealResultSerializer(results, many=True)
        return Response(serializer.data)
