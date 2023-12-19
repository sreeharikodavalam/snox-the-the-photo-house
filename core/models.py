from django.db import models


class FaceDetectionJob(models.Model):
    updated_time = models.DateTimeField(null=True)

    class Meta:
        db_table = 'app_face_detection_schedules'
