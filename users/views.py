from django.contrib.auth.models import make_password
from core.models import CustomUser
from .serializers import LoginSerializer, UserSerializer, SignupSerializer
from django.contrib.auth import authenticate
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .selectors import getAllUsers, getUser
from .services import createUser, deleteUser, updateUser, loginUser


class UserList(APIView):
    def get(self, request, format=None):
        user = getAllUsers()
        serializer = UserSerializer(user, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_data = serializer.validated_data
        user = createUser(user_data["email"], user_data["password"], user_data["role"])
        return Response(user, status=status.HTTP_201_CREATED)


class UserDetail(APIView):
    def get_object(self, pk):
        try:
            return getUser(pk=pk)
        except CustomUser.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserSerializer(data=user)
        if serializer.is_valid():
            return Response(serializer.data)
        else:
            return Response(
                serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def put(self, request, pk, format=None):
        user_data = request.data
        serializer = UserSerializer(data=user_data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]
        hashed_password = make_password(password)
        role = serializer.validated_data["role"]
        updated_user = updateUser(pk, email, hashed_password, role)

        if not updated_user:
            return Response(
                {"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )

        return Response(updated_user)

    def delete(self, request, pk, format=None):
        try:
            deleteUser(pk)
            return Response(
                {"message": "User deleted successfully!"},
                status=status.HTTP_204_NO_CONTENT,
            )
        except Exception as e:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LoginView(APIView):
    def post(self, request, format=None):
        serializer = LoginSerializer(
            data=request.data,
            context={"request": request},
        )
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SignupView(APIView):
    def post(self, request, format=None):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        serializer.save()
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
