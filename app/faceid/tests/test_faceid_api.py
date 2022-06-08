"""
Tests for faceid APIs.
"""
from decimal import Decimal

import tempfile
import os

from PIL import Image

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import (FaceID,)

from faceid.serializers import (
    FaceIDSerializer,
    FaceIDDetailSerializer,
)

FACEID_URL = reverse('faceid:faceid-list')


def detail_url(faceid_id):
    """Create and return a faceid url."""
    return reverse('faceid:faceid-detail', args=[faceid_id])


def image_upload_url(faceid_id):
    """Create and return an image upload URL."""

    return reverse('faceid:faceid-upload-image', args=[faceid_id])


def create_faceid(user, **params):
    """Create and retrun a sample faceid. Helper function"""
    defaults = {
        'title': 'Sample FaceID Title',
        'description': 'Sample description',
    }
    defaults.update(params)

    faceid = FaceID.objects.create(user=user, **defaults)
    return faceid


def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)


class PublicFaceIDAPITests(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required to call API."""
        res = self.client.get(FACEID_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateFaceIDAPITests(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(email='user@example.com', password='test123')
        self.client.force_authenticate(self.user)

    def test_retrieve_faceids(self):
        """Test retrieving a list of faceid."""
        create_faceid(user=self.user)
        create_faceid(user=self.user)

        res = self.client.get(FACEID_URL)

        faceid = FaceID.objects.all().order_by('-id')
        serializer = FaceIDSerializer(faceid, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_faceid_list_limited_to_user(self):
        """Test list of faceid is limited to authenticated user."""
        other_user = create_user(
            email='other@example.com',
            password='password123'
        )
        create_faceid(user=other_user)
        create_faceid(user=self.user)

        res = self.client.get(FACEID_URL)

        faceid = FaceID.objects.filter(user=self.user)
        serializer = FaceIDSerializer(faceid, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_get_faceid_detail(self):
        """Test get faceid detail."""
        faceid = create_faceid(user=self.user)

        url = detail_url(faceid.id)
        res = self.client.get(url)

        serializer = FaceIDDetailSerializer(faceid)
        self.assertEqual(res.data, serializer.data)

    def test_create_faceid(self):
        """Test creating faceid."""
        payload = {
            'title': 'Sample FaceID',
        }
        res = self.client.post(FACEID_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        faceid = FaceID.objects.get(id=res.data['id'])
        for k, v in payload.items():
            self.assertEqual(getattr(faceid, k), v)
        self.assertEqual(faceid.user, self.user)

    def test_full_update(self):
        """ Test full update of faceid."""
        faceid = create_faceid(
            user=self.user,
            title='Sample faceid title',
            description='Sample faceid description'
        )

        payload = {
            'title': 'New faceid title',
            'description': 'new faceid description',
        }

        url = detail_url(faceid.id)
        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        faceid.refresh_from_db()
        for k, v in payload.items():
            self.assertEqual(getattr(faceid, k), v)
        self.assertEqual(faceid.user, self.user)

    def test_update_user_returns_error(self):
        """Test changing the faceid user results in an error."""
        new_user = create_user(
            email='user2@example.com',
            password='test123'
        )
        faceid = create_faceid(user=self.user)
        payload = {'user': new_user.id}

        url = detail_url(faceid.id)
        self.client.patch(url, payload)

        faceid.refresh_from_db()
        self.assertEqual(faceid.user, self.user)

    def test_delete_faceid(self):
        """Test deleting a faceid successfully."""
        faceid = create_faceid(user=self.user)
        url = detail_url(faceid_id=faceid.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(FaceID.objects.filter(id=faceid.id).exists())

    def test_faceid_other_users_faceid_error(self):
        """Test trying to delete another users faceid gives error."""
        new_user = create_user(
            email='user2@example.com',
            password='test123',
        )
        faceid = create_faceid(user=new_user)
        url = detail_url(faceid.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(FaceID.objects.filter(id=faceid.id).exists())


class ImageUploadTests(TestCase):
    """Tests for the image upload API."""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'user@example.com',
            'password123',
        )
        self.client.force_authenticate(self.user)
        self.faceid = create_faceid(user=self.user)

    def tearDown(self):
        # runs after the test completed
        self.faceid.image.delete()

    def test_upload_image(self):
        """Test uploading an image to a faceid."""
        url = image_upload_url(self.faceid.id)
        with tempfile.NamedTemporaryFile(suffix='.jpg') as image_file:
            img = Image.new('RGB', (10, 10))
            img.save(image_file)
            image_file.seek(0)
            payload = {'image': image_file}
            res = self.client.post(url, payload, format='multipart')

        self.faceid.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('image', res.data)
        self.assertTrue(os.path.exists(self.faceid.image.path))

    def test_upload_image_bad_request(self):
        """Test uploading invalid image."""
        url = image_upload_url(self.faceid.id)
        payload = {'image': 'not_an_image'}
        res = self.client.post(url, payload, format='multipart')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
