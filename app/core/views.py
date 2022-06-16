"""
Core views for app.
"""
from io import BytesIO

from deepface import DeepFace
from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiTypes,
)
from faceid.prediction import read_image, preprocess

from rest_framework import serializers


class Compare(object):
    def __init__(self, image1, image2):
        self.image1 = image2
        self.image2 = image2


# create a serializer
class CompareSerializer(serializers.Serializer):
    # initialize fields
    image1 = serializers.FileField()
    image2 = serializers.FileField()


@extend_schema_view(
    post=extend_schema(description='post desc', request=CompareSerializer, responses=OpenApiTypes.UUID),
)
@api_view(['POST'])
def compare_view(request):
    """Gets two separate image and  compares them."""
    print(request.FILES)
    image1 = preprocess(read_image(BytesIO(request.FILES["image1"].read())))
    image2 = preprocess(read_image(BytesIO(request.FILES["image2"].read())))
    model_name = 'VGG-Face'
    result = DeepFace.verify(img1_path=image1, img2_path=image2, model_name=model_name)

    return Response(result)


@api_view(['GET'])
def health_check(request):
    """Returns successful response."""
    return Response({'healthy': True})
