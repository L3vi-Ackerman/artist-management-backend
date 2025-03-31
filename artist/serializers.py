from rest_framework import serializers
from django.utils import timezone
from users.serializers import UserSerializer
from core.models import Artist 

class ArtistSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True, required=False)
    user = UserSerializer()
    name = serializers.CharField(max_length=255)
    dob = serializers.DateField()
    gender = serializers.ChoiceField(choices=Artist.GENDER, default="M")
    address = serializers.CharField(max_length=255)
    first_release_year = serializers.DateField()
    no_of_albumns_released = serializers.IntegerField()
    created_at = serializers.DateTimeField(default=timezone.now, read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

