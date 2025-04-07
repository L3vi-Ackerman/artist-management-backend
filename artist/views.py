from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from core.models import Artist
from .serializers import ArtistSerializer
from .pagination import ArtistPagination
from .selectors import get_paginated_artists, getArtist, getSingleArtist
from users.utils import decode_jwt, getBearerToken
from .services import createArtist, updateArtist, deleteArtist
from users.services import createUser
from rest_framework.permissions import IsAuthenticated

class ArtistList(APIView):
    # permission_classes=[IsAuthenticated]
    authentication_classes = []
    permission_classes = []
    def get(self, request, format=None):
        try:
            paginator = ArtistPagination()
            token = request.headers["Authorization"].split(" ")[1]
            payload = decode_jwt(token)
            user_id = payload.get("id")
           
            artists = get_paginated_artists(request, paginator, userID=user_id)
            print(artists)
            serializer = ArtistSerializer(artists, many=True)
            return paginator.get_paginated_response(serializer.data)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def post(self, request, format=None):
        serializer = ArtistSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        artist_data = serializer.validated_data
        user_data= createUser(artist_data["user"]["email"],artist_data["user"]["password"],artist_data["user"]['role'])
        artist = createArtist(
                user_data["id"],
            artist_data["name"],
            artist_data["dob"],
            artist_data["gender"],
            artist_data["address"],
            artist_data["first_release_year"],
            artist_data["no_of_albumns_released"],
        )
        artist["user"]=user_data
        return Response(artist, status=status.HTTP_201_CREATED)


class ArtistDetail(APIView):
    def get_object(self, pk):
        try:
            return getArtist(pk=pk)
        except Artist.DoesNotExist:
            raise Http404

    
    def get(self, request, pk, format=None):
        artist = getArtist(pk = pk)
        artist = self.get_object(pk)
        serializer = ArtistSerializer(artist)
        return Response(serializer.data)

    def put(self, request,pk, format=None):
        token = request.headers["Authorization"].split(" ")[1]
        payload = decode_jwt(token)
        user_id = payload.get("id")
        user_data = request.data
        serializer = ArtistSerializer(data=user_data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        name = serializer.validated_data["name"]
        dob = serializer.validated_data["dob"]
        gender = serializer.validated_data["gender"]
        address = serializer.validated_data["address"]
        first_release_year = serializer.validated_data["first_release_year"]
        address = serializer.validated_data["address"]
        no_of_albumns_released = serializer.validated_data["no_of_albumns_released"]

        udpated_artist = updateArtist(
            name=name,
            dob = dob,
            gender = gender,
            address =address,
            first_release_year = first_release_year,
            no_of_albumns_released = no_of_albumns_released,
            pk = pk,
            userId=user_id

        )

        if not udpated_artist:
            return Response(
                {"detail": "Artist not found"}, status=status.HTTP_404_NOT_FOUND
            )

        return Response(udpated_artist)

    def delete(self, request, pk, format=None):
        try:
            deleteArtist(pk)
            return Response(
                {"message": "Artist deleted successfully!"},
                status=status.HTTP_204_NO_CONTENT,
            )
        except Exception as e:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ArtistSingleDetail(APIView):
    
    def get(self,request):

        token = request.headers["Authorization"].split(" ")[1]
        payload = decode_jwt(token)
        user_id = payload.get("id")
        artist = getSingleArtist(user_id)
        serializer = ArtistSerializer(artist)
        return Response(serializer.data)


