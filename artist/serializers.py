from rest_framework import serializers
from django.utils import timezone
from users.serializers import UserSerializer
from core.models import Artist 

class ArtistSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True, required=False)
    user = UserSerializer(read_only=True)
    name = serializers.CharField(max_length=255, allow_null=True, required=False)
    dob = serializers.DateField(allow_null=True, required=False)
    gender = serializers.ChoiceField(choices=Artist.GENDER, default="M", allow_null=True, required=False)
    address = serializers.CharField(max_length=255, allow_null=True, required=False)
    first_release_year = serializers.CharField(max_length=4, allow_null=True, required=False)
    no_of_albumns_released = serializers.IntegerField(allow_null=True, required=False)
    created_at = serializers.DateTimeField(default=timezone.now, read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
