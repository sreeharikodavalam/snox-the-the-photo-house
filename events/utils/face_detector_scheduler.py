from django.utils import timezone

from app.models import FaceDetectionJob


def face_detector_scheduler_yy():
    print(f"Running periodic task at {timezone.now()}")
    FaceDetectionJob.objects.create(updated_time=timezone.now())

# Add your task logic here
