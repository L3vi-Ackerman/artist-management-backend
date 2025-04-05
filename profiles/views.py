from abc import update_abstractmethods
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from core.models import Profile
from django.shortcuts import get_object_or_404
from users.utils import decode_jwt
from .serializers import ProfileSerializer
from .selectors import getProfile, getAllProfiles, getSingleProfile
from .services import createProfile, updateProfile, deleteProfile
from users.services import createUser

class ProfileList(APIView):
    def get(self, request, format=None):
       
        print(request)
        profile = getAllProfiles()
        serializer = ProfileSerializer(profile, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        # token = request.headers["Authorization"].split(" ")[1]
        # payload = decode_jwt(token)
        # user_id = payload.get("id")
        serializer = ProfileSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        profile_data = serializer.validated_data
        user_data = createUser(profile_data["user"]["email"], profile_data["user"]["password"],profile_data["user"]["role"])
        print(f'user id: ',user_data['id'])
        profile = createProfile(
                user_data["id"],
            profile_data["first_name"],
            profile_data["last_name"],
            profile_data["phone"],
            profile_data["dob"],
            profile_data["address"],
        )
        profile["user"] = profile_data
        return Response(profile, status=status.HTTP_201_CREATED)


class ProfileDetail(APIView):
    def get_object(self, pk):
        try:
            return getProfile(pk=pk)
        except Profile.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        profile = self.get_object(pk)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        try:
            token = request.headers["Authorization"].split(" ")[1]
            payload = decode_jwt(token)
            user_id = payload.get("id")
        except (KeyError, IndexError):
            return Response({"detail": "Invalid or missing authorization token"}, status=status.HTTP_401_UNAUTHORIZED)

        # Get the existing profile (either using pk or based on user_id)
        try:
            profile_instance = Profile.objects.get(pk=pk)  # Assuming you want to update by pk
        except Profile.DoesNotExist:
            return Response({"detail": "Profile not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProfileSerializer(instance=profile_instance, data=request.data)
        if serializer.is_valid():
            first_name = serializer.validated_data.get('first_name', profile_instance.first_name)
            last_name = serializer.validated_data.get('last_name', profile_instance.last_name)
            address = serializer.validated_data.get('address', profile_instance.address)
            dob = serializer.validated_data.get('dob', profile_instance.dob)
            phone = serializer.validated_data.get('phone', profile_instance.phone)

            updated_profile_data = updateProfile(
                first_name=first_name,
                last_name=last_name,
                address=address,
                dob=dob,
                phone=phone,
                pk=pk,
                userId=user_id  
           )

            if updated_profile_data:
                return Response(updated_profile_data)
            else:
                return Response({"detail": "Failed to update profile"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        try:
            deleteProfile(pk)
            return Response(
                {"message": "Profile deleted successfully!"},
                status=status.HTTP_204_NO_CONTENT,
            )
        except Exception as e:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ProfileSingleDetail(APIView):
    
    def get(self,request):

        token = request.headers["Authorization"].split(" ")[1]
        payload = decode_jwt(token)
        user_id = payload.get("id")
        artist = getSingleProfile(user_id)
        serializer = ProfileSerializer(artist)
        return Response(serializer.data)


