import face_recognition
import numpy as np

from events.models import UserSelfieRegistration, CroppedGalleryFace


def parse_face_encodings(string_value):
    try:
        known_face_encoding_str = string_value
        known_face_encoding_list = [float(x) for x in known_face_encoding_str.split(',')]
        return np.array(known_face_encoding_list).reshape(1, -1)
    except ValueError as e:
        print("f'An error occurred: {str(e)}'")
        return None


def match_selfies(user_selfie_id):
    user_selfie = UserSelfieRegistration.objects.get(pk=user_selfie_id)
    known_face_encoding_np = parse_face_encodings(user_selfie.selfie_embedding)
    matching_result = match_face_encodings(known_face_encoding_np, known_face_encoding_np)
    print(matching_result)

    result = []
    coped_faces = CroppedGalleryFace.objects.all()
    for face in coped_faces:
        face_embeddings = parse_face_encodings(face.face_embedding)
        match_result = match_face_encodings(known_face_encoding_np, face_embeddings)
        if match_result:
            result.append(face.album)
    return result


def match_face_encodings(known_encoding, comparing_encoding, threshold=0.4):
    result = face_recognition.compare_faces(known_encoding, comparing_encoding, tolerance=threshold)
    return result[0]
