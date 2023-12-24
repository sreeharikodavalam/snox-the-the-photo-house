from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import os
import uuid

from django.contrib.auth.models import User

from snoxpro.settings import MEDIA_ROOT


def do_upload_gallery_image(files, gallery_id, user):
    max_width = 4000
    max_height = 4000

    upload_directory = 'events/gallery/collection/' + str(gallery_id) + "/"
    os.makedirs(os.path.dirname(os.path.join(MEDIA_ROOT, upload_directory)), exist_ok=True)

    uploaded_files = []

    for file_data in files:
        img = Image.open(file_data)
        unique_filename = "snox-" + str(uuid.uuid4()) + "-" + str(gallery_id) + ".jpg"
        original_filepath = os.path.join(MEDIA_ROOT, upload_directory, unique_filename)
        media_file_path = upload_directory + unique_filename
        # add_watermark(img, user)
        if img.width > max_width or img.height > max_height:
            # Resize the image
            img.thumbnail((max_width, max_height))

            # Create an in-memory buffer to store the resized image
            resized_buffer = BytesIO()
            img.save(resized_buffer, format='JPEG')

            with open(original_filepath, 'wb') as resized_file:
                resized_file.write(resized_buffer.getvalue())

            uploaded_files.append(media_file_path)
            watermark_with_transparency(MEDIA_ROOT / media_file_path, user)
        else:

            with open(original_filepath, 'wb') as original_file:
                for chunk in file_data.chunks():
                    original_file.write(chunk)

            uploaded_files.append(media_file_path)
            watermark_with_transparency(MEDIA_ROOT / media_file_path, user)

    return uploaded_files


def watermark_with_transparency(image_path, user: User):
    base_image = Image.open(image_path)

    # Open and resize watermark image
    watermark_image = Image.open(user.userprofile.business.watermark)
    watermark_ratio = 0.3
    watermark_width = int(min(base_image.width, base_image.height) * watermark_ratio)
    aspect_ratio = watermark_image.width / watermark_image.height
    watermark_height = int(watermark_width / aspect_ratio)
    watermark_image = watermark_image.resize((watermark_width, watermark_height))

    # Calculate the position to center the watermark
    position = (int(base_image.width - watermark_image.width), int(base_image.height - watermark_image.height))

    # Paste watermark onto base image
    base_image.paste(watermark_image, position, watermark_image)

    # Save the result
    base_image.save(image_path)
