from cv2 import cv2
from io import BytesIO
from azure.cognitiveservices.vision.face.models import FaceAttributeType


def get_detected_faces(face_client, frame):
    ret, buffer = cv2.imencode(".jpg", frame)
    stream = BytesIO(buffer)

    attributes = [FaceAttributeType.smile,
                  FaceAttributeType.emotion]

    detected_faces = face_client.face.detect_with_stream(
        image=stream, return_face_attributes=attributes)

    if not detected_faces:
        raise Exception(
            'No face detected from image')
    return detected_faces
