from whatsapp.models import WhatsappLogSharedPhotos, WhatsappLogWelcomeMessages


def is_welcome_message_send(mobile_number):
    return WhatsappLogWelcomeMessages.objects.filter(mobile_number=mobile_number).exists()


def is_image_send(mobile_number, gallery_image):
    return WhatsappLogSharedPhotos.objects.filter(
        mobile_number=mobile_number,
        gallery_image=gallery_image
    ).exists()

