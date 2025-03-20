from rest_framework import serializers
from django.utils import timezone
from core.models import Artist, CustomUser
from users.selectors import getUser


class ArtistSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    user_id = serializers.IntegerField(required=False)
    user_email = serializers.EmailField(read_only=True)
    name = serializers.CharField(max_length=255)
    dob = serializers.DateField()
    gender = serializers.ChoiceField(choices=Artist.GENDER, default="M")
    address = serializers.CharField(max_length=255)

    first_release_year = serializers.DateField()
    no_of_albumns_released = serializers.IntegerField()
    created_at = serializers.DateTimeField(default=timezone.now, read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        user_id = validated_data.pop("user_id", None)
        if user_id:
            try:
                user = CustomUser.objects.get(pk=user_id)
            except CustomUser.DoesNotExist:
                raise serializers.ValidationError(
                    {"user_id": "User with this ID does not exist."}
                )
        else:
            user = self.context["request"].user

        artist = Artist.objects.create(user=user, **validated_data)
        return artist

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.dob = validated_data.get("dob", instance.dob)
        instance.gender = validated_data.get("gender", instance.gender)
        instance.address = validated_data.get("address", instance.address)
        instance.first_release_year = validated_data.get(
            "first_release_year", instance.first_release_year
        )
        instance.no_of_albumns_released = validated_data.get(
            "no_of_albumns_released", instance.no_of_albumns_released
        )
        instance.save()
        return instance
