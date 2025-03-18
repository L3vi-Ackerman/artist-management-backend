from rest_framework import serializers
from users.serializers import UserSerializer
from core.models import CustomUser, Profile


class ProfileSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(write_only=True, required=False)
    first_name = serializers.CharField(required=True, max_length=255)
    last_name = serializers.CharField(required=True, max_length=255)
    phone = serializers.IntegerField()
    dob = serializers.DateField()
    address = serializers.CharField(max_length=255)

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

        profile = Profile.objects.create(user=user, **validated_data)
        return profile

    def update(self, instance, validated_data):

        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.phone = validated_data.get("phone", instance.phone)
        instance.dob = validated_data.get("dob", instance.dob)
        instance.address = validated_data.get("address", instance.address)
        instance.save()
        return instance

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        user_data = UserSerializer(instance.user).data
        return {"user": user_data, **representation}
