# Importing Azure Face API Dependencies:
import asyncio
import io
import glob
import os
import sys
import time
import uuid
import requests
from urllib.parse import urlparse
from io import BytesIO
from PIL import Image, ImageDraw
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.face.models import TrainingStatusType, Person

# Importing OpenCV Dependency:
from cv2 import cv2

# Importing Services module:
import services


def init_face_api():
    KEY = os.environ.get('CORTEX_KEY')
    ENDPOINT = "https://cortex-face-api.cognitiveservices.azure.com/"
    # Create an authenticated FaceClient.
    face_client = FaceClient(ENDPOINT, CognitiveServicesCredentials(KEY))
    return face_client


async def init_webcam():
    global FRAMES_COUNT

    cap = cv2.VideoCapture(0)

    # Check if the webcam is opened correctly
    if not cap.isOpened():
        raise IOError("Cannot open webcam")

    while True:
        # get frame:
        ret, frame = cap.read()

        # display frame:
        cv2.imshow('Cortex Input', frame)

        # decide whether to analyze:
        if should_analyze(frame):
            # save frame locally:
            # save_frame(frame)

            # analyze frame and consume result:
            r = await analyze_frame(frame)
            consume_result(r)

            # wait for exit:
        c = cv2.waitKey(1)
        if c == 27:
            break

        FRAMES_COUNT += 1

    cap.release()
    cv2.destroyAllWindows()


def save_frame(frame):
    global FRAMES_COUNT

    file_name = os.path.join(os.path.dirname(os.path.abspath(
        __file__)), "frame{}.jpg".format(FRAMES_COUNT))

    if not cv2.imwrite(file_name, frame):
        raise Exception("Could not write frame")


def should_analyze(frame):
    global FRAMES_COUNT
    global FRAMES_ANALYSIS_RATE

    return (FRAMES_COUNT % FRAMES_ANALYSIS_RATE == 0)


async def analyze_frame(frame):
    global face_client
    return services.get_detected_faces(face_client, frame)


def consume_result(result):
    print('Detected Face Info: ')
    for face in result:
        attributes = face.face_attributes
        print("* Emotion:", attributes.emotion)
        print("* Smile:", attributes.smile)
    print()


# Settings:
FRAMES_ANALYSIS_RATE = 20   # this means only 1 in 20 frames get analyzed
FRAMES_COUNT = 0

# initialize app:
face_client = init_face_api()
asyncio.run(init_webcam())
