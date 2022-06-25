"""
Views for the faceid APIs.
"""
import io
import os.path

from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiParameter,
    OpenApiTypes
)
from google.cloud import storage

from rest_framework import (viewsets, mixins, status)
# mixins is required to add additional functionalities to views

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import (FaceID, Foreigner)

from . import serializers
from .serializers import ForeignerSerializer
from django.conf import settings

import uvicorn
from deepface import DeepFace
from .prediction import read_image, preprocess

DOC_ROOT = settings.STATIC_ROOT


class FaceIDViewSet(viewsets.ModelViewSet):
    """View from the manage faceid APIs."""
    serializer_class = serializers.FaceIDDetailSerializer
    queryset = FaceID.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    profile_serializer = serializers.ForeignerSerializer

    def _params_to_ints(self, qs):
        """Convert a list of strings to integers."""
        # 1,2,3
        return [int(str_id) for str_id in qs.split(',')]

    def get_queryset(self):
        """Retrieve faceid for authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by('-id')

    def get_serializer_class(self):
        """Return the serializer class for request."""
        if self.action == 'list':
            return serializers.FaceIDSerializer
        elif self.action == 'upload_image':
            return serializers.FaceIDImageSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """create a new faceid."""
        serializer.save(user=self.request.user)

    @action(methods=['POST'], detail=True, url_path='upload_image')
    def upload_image(self, request, pk=None):
        """Upload an image to faceid."""
        faceid = self.get_object()

        client = storage.Client()
        bucket = client.get_bucket('face_app_dev_bucket')

        profile = Foreigner.objects.all()
        p = profile.filter(user=self.request.user).order_by('-id')
        s = ForeignerSerializer(p, many=True)
        print("=="*5)
        img1 = "uploads/faceid/" + s.data[0]['image'].split('/')[-1]
        blob1 = bucket.get_blob(img1).download_as_string()
        bytes1 = io.BytesIO(blob1)
        imgRead1 = read_image(bytes1)
        preprocess1 = preprocess(imgRead1)


        print("==" * 5)

        serializers = self.get_serializer(faceid, data=request.data)

        if serializers.is_valid():
            print("==" * 3)
            print("==" * 3)
            serializers.save()
            print(serializers.data)
            print("==" * 3)
            img2 = os.path.join("uploads/faceid/", serializers.data['image'].split('/')[-1])
            blob2 = bucket.get_blob(img2).download_as_string()
            bytes2 = io.BytesIO(blob2)
            imgRead2 = read_image(bytes2)
            print(img2)
            print("==" * 3)
            preprocess1 = preprocess(imgRead1)
            preprocess2 = preprocess(imgRead2)
            model_name = 'VGG-Face'
            print(model_name)
            result = DeepFace.verify(img1_path=preprocess1, img2_path=preprocess2, model_name=model_name)
            print(str(result))
            return Response(result, status=status.HTTP_200_OK)

        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


class ForeignerViewSet(viewsets.ModelViewSet):
    """View from the manage Foreigner APIs."""
    serializer_class = serializers.ForeignerSerializer
    queryset = Foreigner.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve faceid for authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by('-id')

    def get_serializer_class(self):
        """Return the serializer class for request."""
        if self.action == 'list':
            return serializers.ForeignerSerializer
        elif self.action == 'upload_image':
            return serializers.ForeignerImageSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """create a new faceid."""
        serializer.save(user=self.request.user)

    @action(methods=['POST'], detail=True, url_path='upload_image')
    def upload_image(self, request, pk=None):
        """Upload an image to faceid."""

        foreigner = self.get_object()
        serializers = self.get_serializer(foreigner, data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_200_OK)

        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
