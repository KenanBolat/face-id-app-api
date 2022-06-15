"""
Database models.
"""
import uuid
import os

from django.conf import settings
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)


def faceid_image_file_path(instance, filename):
    """Generate file path for new faceid image."""
    ext = os.path.splitext(filename)[1]
    filename = f'{uuid.uuid4()}{ext}'

    return os.path.join('uploads', 'faceid', filename)


class UserManager(BaseUserManager):
    """ Manager for users. """

    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user. """
        if not email:
            raise ValueError('User must have an email address')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self.db)

        return user

    def create_superuser(self, email, password):
        """Create and return new super user."""

        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self.db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system."""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    blocked = models.BooleanField(null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Foreigner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=200, null=True)
    image = models.ImageField(default='default.jpg', upload_to=faceid_image_file_path)

    def __str__(self):
        return self.user.name


class FaceID(models.Model):
    """FaceID object."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=255)
    image = models.ImageField(null=True, upload_to=faceid_image_file_path)

    def __str__(self):
        return self.title
