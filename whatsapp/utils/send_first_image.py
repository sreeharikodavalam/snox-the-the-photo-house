import requests
from django.utils import timezone

from events.models import GalleryImage
from whatsapp.contants import INFOBIP_API_KEY, INFOBIP_BASE_URL, INFOBIP_SENDER
from whatsapp.models import WhatsappLogSharedPhotos
from .whatsapp_utils import is_image_send


def send_first_image(mobile_number, image_url, gallery_image):
    if is_image_send(mobile_number, gallery_image=gallery_image):
        return
    payload = {
        "messages":
            [
                {
                    "from": INFOBIP_SENDER,
                    "to": mobile_number,
                    "content": {
                        "templateName": "first_image_delivery",
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

    response = requests.post(INFOBIP_BASE_URL + "/whatsapp/1/message/template", json=payload, headers=headers)
    # print(response.json())
    WhatsappLogSharedPhotos.objects.create(mobile_number=mobile_number, send_time=timezone.now(), gallery_image=gallery_image)
