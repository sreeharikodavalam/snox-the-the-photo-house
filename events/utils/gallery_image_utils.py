import os
from io import BytesIO

import face_recognition
import numpy as np
from PIL import Image

from events.models import CroppedGalleryFace
from events.utils.face_detector import match_new_image_and_send
from snoxpro import settings


def detect_and_crop_faces(gallery_image, padding_percentage=8):
    image_path = gallery_image.album_cover.path

    # Load the image using face_recognition library
    image = face_recognition.load_image_file(image_path)

    # Find all face locations in the image
    face_locations = face_recognition.face_locations(image)

    # Create a directory to store cropped faces
    media_directory = 'events/gallery/faces/' + str(gallery_image.pk) + "/"
    cropped_faces_dir = os.path.join(settings.MEDIA_ROOT, media_directory)
    os.makedirs(cropped_faces_dir, exist_ok=True)
    for i, (top, right, bottom, left) in enumerate(face_locations):
        # Calculate percentage-based padding
        padding_pixels = int(min(image.shape[0] - top, bottom, image.shape[1] - left, right) * padding_percentage / 100)

        # Expand the face bounding box with percentage-based padding
        top = max(0, top - padding_pixels)
        right = min(image.shape[1], right + padding_pixels)
        bottom = min(image.shape[0], bottom + padding_pixels)
        left = max(0, left - padding_pixels)

        # Crop the face with padding
        face_image = Image.fromarray(image[top:bottom, left:right])
        face_file_name = f'album_{gallery_image.pk}_face_{i + 1}.jpg'
        face_image_path = os.path.join(cropped_faces_dir, face_file_name)
        face_image.save(face_image_path)

        # Calculate face embedding using face_recognition
        face_encoding = face_recognition.face_encodings(image, known_face_locations=[(top, right, bottom, left)])[0]
        face_embedding = ",".join(map(str, face_encoding))

        # Save cropped face and its embedding in the database
        saved_face = CroppedGalleryFace.objects.create(gallery_image=gallery_image, image=media_directory + face_file_name, face_embedding=face_embedding)
        match_new_image_and_send(face=saved_face, image=gallery_image)

    return True


def get_face_embedding(image_bytes):
    try:
        # Use BytesIO to create a file-like object from the binary data
        image_file = BytesIO(image_bytes)

        # Open the image using Pillow
        pil_image = Image.open(image_file)

        # Convert the image to RGB if it's not in that mode
        pil_image = pil_image.convert("RGB")

        # Get face encodings using face_recognition
        face_encodings = face_recognition.face_encodings(np.array(pil_image))

        if face_encodings:
            # Convert the face encoding to a list for storage in the database
            return face_encodings[0].tolist()

    except Exception as e:
        # Log or return a more descriptive error message
        print(f"An error occurred: {e}")

    return None
