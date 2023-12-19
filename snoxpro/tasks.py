from celery import shared_task
from django.utils import timezone

from app.models import FaceDetectionJob


@shared_task
def face_detection_jobs():
    FaceDetectionJob.objects.create(updated_time=timezone.now())


@shared_task
def face_detection_periodic_task():
    face_detection_jobs.delay()
