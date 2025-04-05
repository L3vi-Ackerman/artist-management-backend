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
        profile = request.data
        serializer = ProfileSerializer(profile)

        token = request.headers["Authorization"].split(" ")[1]
        payload = decode_jwt(token)
        user_id = payload.get("id")
        role = payload.get("role")

        updated_profile = updateProfile(
            pk,
            user_id,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            dob=dob,
            address=address,
        )

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        first_name = serializer.validated_data["first_name"]
        last_name = serializer.validated_data["last_name"]
        phone = serializer.validated_data["phone"]
        dob = serializer.validated_data["dob"]
        address = serializer.validated_data["address"]

        if not updated_profile:
            return Response(
                {"detail": "Profile not found"}, status=status.HTTP_404_NOT_FOUND
            )
        return Response(updated_profile)

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


