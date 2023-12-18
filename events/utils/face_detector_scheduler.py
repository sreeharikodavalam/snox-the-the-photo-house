from django.utils import timezone
from django.utils.datetime_safe import datetime

from app.models import FaceDetectionJobs


def face_detector_scheduler_yy():
    print(f"Running periodic task at {datetime.now()}")
    FaceDetectionJobs.objects.create(updated_time=timezone.now())

# Add your task logic here
