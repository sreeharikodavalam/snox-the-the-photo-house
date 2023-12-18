from django.db import models


class FaceDetectionJobs(models.Model):
    updated_time = models.DateTimeField(null=True)
