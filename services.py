def get_detected_faces(face_client, frame):
    detected_faces = face_client.face.detect_with_stream(frame)
    if not detected_faces:
        raise Exception(
            'No face detected from image')
    return detected_faces
