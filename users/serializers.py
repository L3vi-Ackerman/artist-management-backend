from rest_framework import serializers,status
from core.models import CustomUser, Artist
from django.contrib.auth import authenticate

from .services import loginUser
from .utils import create_jwt
from django.contrib.auth.hashers import make_password
from rest_framework.response import Response



class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, required=True)
    role = serializers.ChoiceField(choices=CustomUser.ROLES)
    is_active = serializers.BooleanField(read_only=True)

   

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            raise serializers.ValidationError("Both email and password are required")
        user = loginUser(email, password)

        if user is None:
            raise serializers.ValidationError("Invalid credentials!")
        token = create_jwt(user)
        return {"token": token}

class SignUpSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    role = serializers.ChoiceField(choices = CustomUser.ROLES)


class ArtistSignupSerializer(serializers.Serializer):

    user = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    role = serializers.ChoiceField(choices=CustomUser.ROLES)
    name = serializers.CharField(max_length=255)
    phone = serializers.IntegerField()
    dob = serializers.DateField()
    gender = serializers.ChoiceField(choices=Artist.GENDER)
    first_release_year = serializers.DateField()
    no_of_albumns_released = serializers.IntegerField()


class ManagerSignUpSerializer(serializers.Serializer):

    user = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    role = serializers.ChoiceField(choices=CustomUser.ROLES)
    first_name = serializers.CharField(required=True, max_length=255)

    last_name = serializers.CharField(required=True, max_length=255)
    address = serializers.CharField(max_length=255)
    dob = serializers.DateField()
    phone = serializers.IntegerField()
