"""
Test for models.
"""
from unittest.mock import patch
from decimal import Decimal

from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


def create_user(email='test@example.com', password='testpass'):
    """create and return new user."""
    return get_user_model().objects.create_user(
        email=email,
        password=password)


class ModelTest(TestCase):
    """Test models."""

    def test_create_user_with_email(self):
        """Test creating a user an email is successful."""
        email = 'test@test.com'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test email normalized"""
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.com', 'TEST3@example.com'],
            ['test4@example.com', 'test4@example.com']
        ]

        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, 'sample123')
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_rasises_error(self):
        """Test that creating a user without an email raises a ValueError"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'test123')

    def test_create_super_user(self):
        """Test creating super user."""
        user = get_user_model().objects.create_superuser(
            'test@example.com',
            'test123'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_faceid(self):
        """Test creating a faceid is successful."""
        user = get_user_model().objects.create_user(
            'test@example.com',
            'testpass123',
        )
        faceid = models.FaceID.objects.create(
            user=user,
            title='Sample faceid name',
            description='Sample faceid description',
        )

        self.assertEqual(str(faceid), faceid.title)

    @patch('core.models.uuid.uuid4')
    def test_faceid_file_name_uuid(self, mock_uuid):
        """Test generating image path."""
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid
        file_path = models.faceid_image_file_path(None, 'example.jpg')

        self.assertEqual(file_path, f'uploads/faceid/{uuid}.jpg')
