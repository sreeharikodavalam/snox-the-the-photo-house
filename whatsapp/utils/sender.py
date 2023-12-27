from snoxpro.settings import BASE_URL
from .whatsapp_utils import is_send_first_image
from .send_first_image import send_first_image
from .send_additional_image import send_additional_image
from events.models import UserSelfieRegistration, GalleryImage


def send_images_to_user(user_selfie: UserSelfieRegistration, gallery_image_list):
    send_once = is_send_first_image(f"91{user_selfie.mobile_number}")
    for image in gallery_image_list:
        send_single_image_to_user(user=user_selfie, image=image, send_once=send_once)
        # # image_url = f"{BASE_URL}{image.image.url}"
        # image_url = "https://app.snoxpro.com/media/events/gallery/collection/1/1_7553cfa6-e9ff-4fec-ac7d-bc041281a1eb_IMG_6783.jpg"
        # print(f"Mobile:{user_selfie.mobile_number} | ID:{image.pk} | URL:{image_url}")
        # if send_once is False:
        #     send_once = True
        #     send_first_image(f"91{user_selfie.mobile_number}", image_url, gallery_image=image)
        # else:
        #     send_additional_image(f"91{user_selfie.mobile_number}", image_url=image_url, gallery_image=image)


def send_single_image_to_user(user: UserSelfieRegistration, image: GalleryImage, send_once=None):
    if send_once is None:
        send_once = is_send_first_image(f"91{user.mobile_number}")
    image_url = f"{BASE_URL}{image.image.url}"
    print(f"Mobile:{user.mobile_number} | ID:{image.pk} | URL:{image_url}")
    if send_once is False:
        send_first_image(f"91{user.mobile_number}", image_url, gallery_image=image)
    else:
        send_additional_image(f"91{user.mobile_number}", image_url=image_url, gallery_image=image)
