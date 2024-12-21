import json
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status


from library.tasks import generate_report
import os

class ReportView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        # Get the latest report file
        reports_dir = "reports/"
        try:
            latest_report = sorted(os.listdir(reports_dir))[-1]
            with open(os.path.join(reports_dir, latest_report), "r") as report_file:
                report_data = report_file.read()
            return Response(json.loads(report_data), status=status.HTTP_200_OK)
        except (IndexError, FileNotFoundError):
            return Response({"error": "No reports available."}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        # Trigger the Celery task
        result = generate_report.delay()
        return Response(
            {"message": "Report generation started.", "task_id": result.id},
            status=status.HTTP_202_ACCEPTED,
        )