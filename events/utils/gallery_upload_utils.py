from PIL import Image
from io import BytesIO
import os
import uuid

from snoxpro.settings import MEDIA_ROOT


def do_upload_gallery_image(files, gallery_id):
    max_width = 2000
    max_height = 2000

    upload_directory = 'events/gallery/collection/' + str(gallery_id) + "/"
    os.makedirs(os.path.dirname(os.path.join(MEDIA_ROOT, upload_directory)), exist_ok=True)

    uploaded_files = []

    for file_data in files:
        img = Image.open(file_data)
        unique_filename = "snox-" + str(uuid.uuid4()) + "-" + str(gallery_id) + ".jpg"
        original_filepath = os.path.join(MEDIA_ROOT, upload_directory, unique_filename)
        media_file_path = upload_directory + unique_filename

        if img.width > max_width or img.height > max_height:
            # Resize the image
            img.thumbnail((max_width, max_height))

            # Create an in-memory buffer to store the resized image
            resized_buffer = BytesIO()
            img.save(resized_buffer, format='JPEG')

            with open(original_filepath, 'wb') as resized_file:
                resized_file.write(resized_buffer.getvalue())

            uploaded_files.append(media_file_path)
        else:

            with open(original_filepath, 'wb') as original_file:
                for chunk in file_data.chunks():
                    original_file.write(chunk)

            uploaded_files.append(media_file_path)

    return uploaded_files
