from whatsapp.models import WhatsappLogSharedPhoto, WhatsappLogWelcomeMessage, WhatsappSender
from datetime import timedelta
from django.utils import timezone


def is_welcome_message_send(mobile_number):
    return WhatsappLogWelcomeMessage.objects.filter(mobile_number=mobile_number).exists()


def is_image_send(mobile_number, gallery_image):
    return WhatsappLogSharedPhoto.objects.filter(
        mobile_number=mobile_number,
        gallery_image=gallery_image
    ).exists()


def is_send_first_image(mobile_number):
    return WhatsappLogSharedPhoto.objects.filter(mobile_number=mobile_number).exists()


def get_sender_number(mobile_number):
    twenty_four_hours_ago = timezone.now() - timedelta(hours=24)
    last_message = WhatsappLogWelcomeMessage.objects.filter(
        mobile_number=mobile_number,
        send_time__gte=twenty_four_hours_ago
    ).first()
    print(f"Last message by number : {last_message.mobile_number}")
    if last_message and last_message.sender:
        return last_message.sender.sender_number
    else:
        senders = WhatsappSender.objects.all()
        for sender in senders:
            count = WhatsappLogWelcomeMessage.objects.filter(
                sender=sender,
                send_time__gte=twenty_four_hours_ago
            ).count()
            if count < 245 or count is None:
                return sender.sender_number
    return None
