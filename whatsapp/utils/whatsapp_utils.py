from whatsapp.models import WhatsappLogSharedPhoto, WhatsappLogWelcomeMessage


def is_welcome_message_send(mobile_number):
    return WhatsappLogWelcomeMessage.objects.filter(mobile_number=mobile_number).exists()


def is_image_send(mobile_number, gallery_image):
    return WhatsappLogSharedPhoto.objects.filter(
        mobile_number=mobile_number,
        gallery_image=gallery_image
    ).exists()

