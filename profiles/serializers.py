from rest_framework import serializers
from users.serializers import UserSerializer
from core.models import CustomUser, Profile
from django.utils import timezone


class ProfileSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True, required=False)
    user = UserSerializer(allow_null=True)
    first_name = serializers.CharField(required=True, max_length=255)
    last_name = serializers.CharField(required=True, max_length=255)
    phone = serializers.CharField(max_length=10)
    dob = serializers.DateField()
    address = serializers.CharField(max_length=255)
    created_at = serializers.DateTimeField(default=timezone.now,read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
