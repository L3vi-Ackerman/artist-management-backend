from rest_framework import serializers
from core.models import CustomUser, Artist
from django.contrib.auth import authenticate
from .utils import create_jwt


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, required=True)
    role = serializers.ChoiceField(choices=CustomUser.ROLES)
    is_superuser = serializers.BooleanField(read_only=True)
    is_staff = serializers.BooleanField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    date_joined = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            raise serializers.ValidationError("Both email and password are required")
        user = authenticate(email=email, password=password)

        if user is None:
            raise serializers.ValidationError("Invalid Credentials!")

        token = create_jwt(user)
        return token


class SignupSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    role = serializers.ChoiceField(choices=CustomUser.ROLES)
    first_name = serializers.CharField(required=True, max_length=255)
    last_name = serializers.CharField(required=True, max_length=255)
    user = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())
    phone = serializers.IntegerField()
    dob = serializers.DateField()
    address = serializers.CharField(max_length=255)
    dob = serializers.DateField()
    gender = serializers.ChoiceField(choices=Artist.GENDER)
    first_release_year = serializers.DateField()
    no_of_albumns_released = serializers.IntegerField()
