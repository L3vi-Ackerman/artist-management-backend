from rest_framework import serializers
from users.serializers import UserSerializer
from core.models import CustomUser, Profile
from django.utils import timezone


class ProfileSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    user = UserSerializer(read_only=True)
    first_name = serializers.CharField(required=False, max_length=255,allow_null=True)
    last_name = serializers.CharField(required=False, max_length=255,allow_null=True)
    phone = serializers.CharField(allow_null=True,required=False)
    dob = serializers.DateField(allow_null=True, required=False)
    address = serializers.CharField(max_length=255,allow_null=True,required=False)
    created_at = serializers.DateTimeField(default=timezone.now,read_only=True, required=False)
    updated_at = serializers.DateTimeField(read_only=True, required=False, allow_null=True)
