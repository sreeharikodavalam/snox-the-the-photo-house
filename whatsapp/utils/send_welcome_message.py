
import requests
from django.utils import timezone

from whatsapp.contants import INFOBIP_API_KEY, INFOBIP_BASE_URL
from whatsapp.models import WhatsappLogWelcomeMessage,WhatsappSender
from .whatsapp_utils import is_welcome_message_send, get_sender_number


def send_welcome_message(mobile_number, user_name, event_name):
    print(user_name)
    print(event_name)
    sender_number = get_sender_number(mobile_number)
    if is_welcome_message_send(mobile_number) or sender_number is None:
        return
    payload = {
        "messages":
            [
                {
                    "from": sender_number,
                    "to": mobile_number,
                    "content": {
                        "templateName": "event_registration_result",
                        "templateData": {
                            "body": {
                                "placeholders": [user_name.strip(), event_name.strip()]
                            },
                            "header": {
                                "type": "IMAGE",
                                "mediaUrl": "https://app.snoxpro.com/static/img/logo.png"
                            },
                        },
                        "language": "en"
                    }
                }
            ]
    }

    headers = {
        'Authorization': INFOBIP_API_KEY,
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    response = requests.post(INFOBIP_BASE_URL + "/whatsapp/1/message/template", json=payload, headers=headers)
    print(response.json())
    sender = WhatsappSender.objects.filter(sender_number=sender_number).first()
    WhatsappLogWelcomeMessage.objects.create(mobile_number=mobile_number, sender=sender, send_time=timezone.now())
