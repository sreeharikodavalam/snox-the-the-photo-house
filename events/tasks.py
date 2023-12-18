import logging
from celery import shared_task

from django.utils import timezone

from app.models import FaceDetectionJobs

logger = logging.getLogger(__name__)


@shared_task
def my_periodic_task():
    try:
        logger.error("Running periodic task---")
        FaceDetectionJobs.objects.create(updated_time=timezone.now())
    except Exception as e:
        logger.error(f"Error in my_periodic_task: {e}")
