from celery import shared_task
from snoxpro.celery import app
from django.utils import timezone


@app.task
def face_detection_jobs():
    from core.models import FaceDetectionJob
    FaceDetectionJob.objects.create(updated_time=timezone.now())


@shared_task
def face_detection_periodic_task():
    face_detection_jobs.delay()
