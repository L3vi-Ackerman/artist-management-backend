from rest_framework import serializers
from django.utils import timezone
from core.models import Artist, CustomUser
from users.selectors import getUser


class ArtistSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    user_id = serializers.IntegerField(required=False)
    user_email = serializers.EmailField(read_only=True)
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

    # def to_representation(self, instance):
    #     print(type(instance))
    #     representation = super().to_representation(instance)
    #     user_id = representation.get("user_id")
    #     if user_id:
    #         user = getUser(pk=user_id)
    #         if user:
    #             representation["user_email"] = user.get("email")  # get email from dict.
    #         else:
    #             representation["user_email"] = None

    #     representation["artist_id"] = instance.id
    #     return representation
