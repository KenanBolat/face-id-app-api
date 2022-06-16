"""
Serializers for FaceID API.
"""
from rest_framework import serializers

from core.models import (FaceID, Foreigner)


class FaceIDSerializer(serializers.ModelSerializer):
    """Serializer for faceid."""

    class Meta:
        model = FaceID
        fields = ['id',
                  'title', 'image', ]
        read_only_fields = ['id']

    def create(self, validated_data):
        """Create a faceid."""
        faceid = FaceID.objects.create(**validated_data)
        return faceid

    def update(self, instance, validated_data):
        """Update faceid."""
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class FaceIDDetailSerializer(FaceIDSerializer):
    """Serializer for faceid detail view."""

    class Meta(FaceIDSerializer.Meta):
        fields = FaceIDSerializer.Meta.fields + ['image']


class FaceIDImageSerializer(serializers.ModelSerializer):
    """Serializer for uploading image to FaceID."""

    class Meta:
        model = FaceID
        fields = ['id', 'image']
        read_only_fields = ['id']
        extra_kwargs = {'image': {'required': 'True'}}


class ForeignerSerializer(serializers.ModelSerializer):
    """Serializer for foreigner."""

    class Meta:
        model = Foreigner
        fields = ['id',
                  'phone', 'image', ]
        read_only_fields = ['id']

    def create(self, validated_data):
        """Create a faceid."""
        foreigner = Foreigner.objects.create(**validated_data)
        return foreigner

    def update(self, instance, validated_data):
        """Update foreigner."""
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class ForeignerDetailSerializer(ForeignerSerializer):
    """Serializer for faceid detail view."""

    class Meta(ForeignerSerializer.Meta):
        fields = ForeignerSerializer.Meta.fields + ['image', 'phone']


class ForeignerImageSerializer(serializers.ModelSerializer):
    """Serializer for uploading image to FaceID."""

    class Meta:
        model = FaceID
        fields = ['id', 'image']
        read_only_fields = ['id']
        extra_kwargs = {'image': {'required': 'True'}}


