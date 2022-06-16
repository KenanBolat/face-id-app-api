"""
Core views for app.
"""
from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiParameter,
    OpenApiTypes,
    OpenApiExample,
)

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
    get=extend_schema(description='get desc', responses={}),
    post=extend_schema(description='post desc', request=CompareSerializer, responses=OpenApiTypes.UUID),
)
@api_view(['POST'])
def health_check(request):
    """Returns successful response."""
    image1 = request.data.get('image1')
    image2 = request.data.get('image2')
    print(image1)
    print(image2)
    return Response({'healthy': True})
