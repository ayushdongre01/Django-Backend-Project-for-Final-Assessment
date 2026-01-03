import uuid
from datetime import datetime
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from deals.models import ScanJob, DealResult
from deals.api.serializers import ScanJobSerializer, DealResultSerializer

@method_decorator(csrf_exempt, name="dispatch")
class StartScanAPIView(APIView):
    def post(self, request):
        scan_job = ScanJob.objects.create(
            id=str(uuid.uuid4()),
            status="RUNNING",
            started_at=datetime.utcnow(),
        )

        serializer = ScanJobSerializer(scan_job)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


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
