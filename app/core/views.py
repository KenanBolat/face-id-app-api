"""
Core views for app.
"""
import io
import os
import uuid

from deepface import DeepFace
from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiTypes,
)
from faceid.prediction import read_image, preprocess
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from google.cloud import storage

from rest_framework import serializers


def faceid_image_file_path(filename):
    """Generate file path for new faceid image."""
    ext = os.path.splitext(filename)[1]
    filename = f'{uuid.uuid4()}{ext}'

    return os.path.join('uploads', 'faceid', filename)


class Compare(object):
    def __init__(self, image1, image2):
        self.image1 = image2
        self.image2 = image2


# create a serializer
class CompareSerializer(serializers.Serializer):
    # initialize fields
    image1 = serializers.ImageField()
    image2 = serializers.ImageField()


@extend_schema_view(
    post=extend_schema(description='post desc',
                       request=CompareSerializer,
                       responses=OpenApiTypes.UUID),
)
@api_view(['POST'])
def compare_view(request):
    """Gets two separate image and  compares them."""
    print(request.FILES)

    print("==" * 5)
    client = storage.Client()
    bucket = client.get_bucket('face_app_dev_bucket')

    path = default_storage.save('img1.png',
                                ContentFile(request.FILES["image1"].read()))

    blob = bucket.get_blob(path).download_as_string()
    bytes = io.BytesIO(blob)
    imgRead1 = read_image(bytes)
    preprocess1 = preprocess(imgRead1)

    path2 = default_storage.save('img2.png',
                                 ContentFile(request.FILES["image2"].read()))
    print(path2)
    blob2 = bucket.get_blob(path2).download_as_string()
    bytes2 = io.BytesIO(blob2)
    imgRead2 = read_image(bytes2)
    preprocess2 = preprocess(imgRead2)

    model_name = 'VGG-Face'
    result = DeepFace.verify(img1_path=preprocess1,
                             img2_path=preprocess2,
                             model_name=model_name)
    print(result)

    return Response(result)


@api_view(['GET'])
def health_check(request):
    """Returns successful response."""
    return Response({'healthy': True})
