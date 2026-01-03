from django.urls import path
from deals.api.views import (
    StartScanAPIView,
    ScanStatusAPIView,
    ScanResultsAPIView,
)

urlpatterns = [
    path("scan/start/", StartScanAPIView.as_view()),
    path("scan/status/<str:scan_job_id>/", ScanStatusAPIView.as_view()),
    path("scan/results/<str:scan_job_id>/", ScanResultsAPIView.as_view()),
]
