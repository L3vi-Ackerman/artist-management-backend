from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from core.models import Profile
from .serializers import ProfileSerializer
from .selectors import getProfile, getAllProfiles
from .services import createProfile


class ProfileList(APIView):
    def get(self, request, format=None):
        profile = getAllProfiles()
        serializer = ProfileSerializer(profile, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):

        serializer = ProfileSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        profile_data = serializer.validated_data
        profile = createProfile(
            profile_data["user_id"],
            profile_data["first_name"],
            profile_data["last_name"],
            profile_data["phone"],
            profile_data["dob"],
            profile_data["address"],
        )
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
        profile = self.get_object(pk)
        serializer = ProfileSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        profile = self.get_object(pk)
        profile.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
