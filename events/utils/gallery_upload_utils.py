from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import os
import uuid

from django.contrib.auth.models import User

from events.models import GalleryImage
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
        thumbnail_path = generate_thumbnail(img, unique_filename, upload_directory)
        # add_watermark(img, user)
        if img.width > max_width or img.height > max_height:
            # Resize the image
            img.thumbnail((max_width, max_height))

            # Create an in-memory buffer to store the resized image
            resized_buffer = BytesIO()
            img.save(resized_buffer, format='JPEG')

            with open(original_filepath, 'wb') as resized_file:
                resized_file.write(resized_buffer.getvalue())

            uploaded_files.append({'image': media_file_path, 'thumbnail': thumbnail_path})
            watermark_with_transparency(MEDIA_ROOT / media_file_path, user)
        else:

            with open(original_filepath, 'wb') as original_file:
                for chunk in file_data.chunks():
                    original_file.write(chunk)

            uploaded_files.append({'image': media_file_path, 'thumbnail': thumbnail_path})
            watermark_with_transparency(MEDIA_ROOT / media_file_path, user)

    return uploaded_files


def generate_thumbnail(img, file_name, base_directory):
    thumbnail = img.copy()
    thumbnail.thumbnail((512, 512), )
    thumbnail_name = f"thumbnail_{file_name}"
    thumbnail_filepath = os.path.join(MEDIA_ROOT / base_directory , thumbnail_name)
    thumbnail.save(thumbnail_filepath, format='JPEG', quality=85)
    return f"{base_directory}{thumbnail_name}"


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


def fix_gallery_thumbnails(gallery_images):
    for temp_img in gallery_images:
        upload_directory = 'events/gallery/collection/' + str(temp_img.gallery.pk) + "/"
        print(f"Up dir : {upload_directory}")
        file_name = os.path.basename(MEDIA_ROOT / temp_img.image.name)

        print(f"File name : {file_name}")
        img = Image.open(temp_img.image.path)
        if img:
            thumb = generate_thumbnail(img=img, file_name=file_name, base_directory=upload_directory)
            gal_img = GalleryImage.objects.filter(pk=temp_img.pk).first()
            gal_img.image_thumbnail = thumb
            gal_img.save()
