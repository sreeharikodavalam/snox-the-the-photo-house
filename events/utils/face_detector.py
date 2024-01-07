import face_recognition
import numpy as np
from whatsapp.utils.sender import send_images_to_user, send_single_image_to_user

from events.models import UserSelfieRegistration, CroppedGalleryFace, GalleryImage


def match_new_image_and_send(face: CroppedGalleryFace, image: GalleryImage):
    known_face_encoding_np = parse_face_encodings(face.face_embedding)
    users = UserSelfieRegistration.objects.filter(event=image.gallery.event)
    for user in users:
        face_embeddings = parse_face_encodings(user.selfie_embedding)
        match_result = match_face_encodings(known_face_encoding_np, face_embeddings)
        if match_result:
            send_single_image_to_user(user=user, image=image)
            break


def match_selfies_and_send(user_selfie_id):
    user_selfie = UserSelfieRegistration.objects.get(pk=user_selfie_id, )
    known_face_encoding_np = parse_face_encodings(user_selfie.selfie_embedding)
    result = []
    event = user_selfie.event
    gallery_images = GalleryImage.objects.filter(gallery__event=event)
    for image in gallery_images:
        cropped_faces = image.get_faces()
        for face in cropped_faces:
            face_embeddings = parse_face_encodings(face.face_embedding)
            match_result = match_face_encodings(known_face_encoding_np, face_embeddings)
            if match_result:
                result.append(image)
                break
    if result is not None:
        send_images_to_user(user_selfie=user_selfie, gallery_image_list=result)


def parse_face_encodings(string_value):
    try:
        known_face_encoding_str = string_value
        known_face_encoding_list = [float(x) for x in known_face_encoding_str.split(',')]
        return np.array(known_face_encoding_list).reshape(1, -1)
    except ValueError as e:
        print("f'An error occurred: {str(e)}'")
        return None


def match_face_encodings(known_encoding, comparing_encoding, threshold=0.4):
    if not known_encoding or not comparing_encoding:
        return False
    # Compare face encodings
    result = face_recognition.compare_faces(known_encoding, comparing_encoding, tolerance=0.5)

    # Additional checks
    if result and face_recognition.face_distance(known_encoding, comparing_encoding)[0] < threshold:
        return True
    else:
        return False
