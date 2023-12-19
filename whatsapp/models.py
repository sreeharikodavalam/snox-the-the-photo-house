from django.db import models

from events.models import GalleryImage


class WhatsappLogSharedPhoto(models.Model):
    mobile_number = models.CharField(max_length=34)
    gallery_image = models.ForeignKey(GalleryImage, on_delete=models.CASCADE)
    send_time = models.DateTimeField()

    class Meta:
        db_table = 'whatsapp_log_photo_share'


class WhatsappLogWelcomeMessage(models.Model):
    mobile_number = models.CharField(max_length=34)
    send_time = models.DateTimeField()

    class Meta:
        db_table = 'whatsapp_log_welcome_message'
