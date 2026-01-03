from django.urls import path
from deals.api.views import (
    StartScanAPIView,
    ScanJobListAPIView,
    ScanJobDetailAPIView,
    ScanJobResultsAPIView,
)

urlpatterns = [
    path("scan/start/", StartScanAPIView.as_view()),
    path("scan/jobs/", ScanJobListAPIView.as_view()),
    path("scan/jobs/<uuid:id>/", ScanJobDetailAPIView.as_view()),
    path("scan/jobs/<uuid:id>/results/", ScanJobResultsAPIView.as_view()),
]
