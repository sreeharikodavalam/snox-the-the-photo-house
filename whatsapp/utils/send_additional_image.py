import requests
from django.utils import timezone

from whatsapp.contants import INFOBIP_API_KEY, INFOBIP_BASE_URL
from whatsapp.models import WhatsappLogSharedPhoto
from whatsapp.utils.whatsapp_utils import is_image_send, get_sender_number


def send_additional_image(mobile_number, image_url, gallery_image):
    sender_number = get_sender_number(mobile_number)
    if is_image_send(mobile_number, gallery_image=gallery_image) or sender_number is None:
        return
    payload = {
        "messages":
            [
                {
                    "from": sender_number,
                    "to": mobile_number,
                    "content": {
                        "templateName": "additional_image_delivery",
                        "templateData": {
                            "body": {
                                "placeholders": []
                            },
                            "header": {
                                "type": "IMAGE",
                                "mediaUrl": image_url
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

    try:
        response = requests.post(INFOBIP_BASE_URL + "/whatsapp/1/message/template", json=payload, headers=headers)
        print(response.json())
    except Exception as e:
        print(f"Whatsapp send error {e}")
    WhatsappLogSharedPhoto.objects.create(mobile_number=mobile_number, gallery_image=gallery_image, send_time=timezone.now())
