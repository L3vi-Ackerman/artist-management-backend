from rest_framework import serializers
from django.utils import timezone
from core.models import Artist
from users.serializers import UserSerializer
from core.models import CustomUser


class ArtistSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(write_only=True, required=False)
    dob = serializers.DateField()
    gender = serializers.ChoiceField(choices=Artist.GENDER, default="M")
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

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        user_data = UserSerializer(instance.user).data
        return {"user": user_data, **representation}
