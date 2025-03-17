from rest_framework import serializers
from django.utils import timezone
from .models import Artist, CustomUser
from users.serializers import UserSerializer


class ArtistSerializer(serializers.Serializer):
    user = UserSerializer()
    dob = serializers.DateField()
    gender = serializers.ChoiceField(choices=Artist.GENDER, default="M")
    first_release_year = serializers.DateField()
    no_of_albumns_released = serializers.IntegerField()
    created_at = serializers.DateTimeField(default=timezone.now, read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        user_data = validated_data.pop("user")
        user = CustomUser.objects.create(**user_data)
        artist = Artist.objects.create(user=user, **validated_data)
        return artist

    def update(self, instance, validated_data):
        user_data = validated_data.pop("user", None)

        if user_data:
            instance.user.email = user_data.get("email", instance.user.email)
            instance.user.role = user_data.get("role", instance.user.role)
            instance.user.save()

        instance.dob = validated_data.get("dob", instance.dob)
        instance.gender = validated_data.get("gender", instance.gender)
        instance.first_release_year = validated_data.get(
            "first_release_year", instance.first_release_year
        )
        instance.no_of_albumns_released = validated_data.get(
            "no_of_albumns_released", instance.no_of_albumns_released
        )

        instance.save()
        return instance
