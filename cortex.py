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

# This key will serve all examples in this document.
KEY = os.environ.get('CORTEX_KEY')

# This endpoint will be used in all examples in this quickstart.
ENDPOINT = "https://cortex-face-api.cognitiveservices.azure.com/"
