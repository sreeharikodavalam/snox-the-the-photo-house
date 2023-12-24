from django.db import models

from events.models import GalleryImage


class WhatsappSender(models.Model):
    sender_number = models.CharField(max_length=34)

    class Meta:
        db_table = 'whatsapp_sender_number'

    def __str__(self):
        return self.sender_number


class WhatsappLogSharedPhoto(models.Model):
    mobile_number = models.CharField(max_length=34)
    gallery_image = models.ForeignKey(GalleryImage, on_delete=models.CASCADE)
    send_time = models.DateTimeField()

    class Meta:
        db_table = 'whatsapp_log_photo_share'


class WhatsappLogWelcomeMessage(models.Model):
    mobile_number = models.CharField(max_length=34)
    sender = models.ForeignKey(WhatsappSender, on_delete=models.CASCADE, null=True)
    send_time = models.DateTimeField()

    class Meta:
        db_table = 'whatsapp_log_welcome_message'
