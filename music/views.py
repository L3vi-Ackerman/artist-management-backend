from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from core.models import Music, Artist
from users.utils import decode_jwt, getBearerToken
from .serializers import MusicSerializer
from .services import (
    createMusic,
    updateMusic,
    deleteMusic,
)
from .selectors import getAllMusic, getMusic


class MusicList(APIView):
    def get(self, request, format=None):
        music_data = getAllMusic()
        serialized_data = []
        for item in music_data:
            artist_data = {
                "id": item.get("artist_id"),
                "name": item.get("artist_name"),
                "dob": str(item.get("artist_dob")),
                "gender": item.get("artist_gender"),
                "address": item.get("artist_address"),
                "first_release_year": item.get("artist_first_release_year"),
                "no_of_albumns_released": item.get("artist_no_of_albumns_released"),
                "created_at": item.get("artist_created_at").isoformat() + "Z" if item.get("artist_created_at") else None,
                "updated_at": item.get("artist_updated_at").isoformat() + "Z" if item.get("artist_updated_at") else None,
            }
            music_item = {
                "id": item.get("music_id"),
                "title": item.get("title"),
                "album_name": item.get("album_name"),
                "genre": item.get("genre"),
                "created_at": item.get("music_created_at").isoformat() + "Z" if item.get("music_created_at") else None,
                "updated_at": item.get("music_updated_at").isoformat() + "Z" if item.get("music_updated_at") else None,
                "artist": artist_data,
            }
            serialized_data.append(music_item)

        serializer = MusicSerializer(serialized_data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = MusicSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        music_data = serializer.validated_data
        music = createMusic(
            music_data["artist_id"].id,
            music_data["title"],
            music_data["album_name"],
            music_data["genre"],
        )
        return Response(music, status=status.HTTP_201_CREATED)


class MusicDetail(APIView):
    def get_object(self, pk):
        try:
            return getMusic(pk=pk)
        except Music.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        music = self.get_object(pk)
        serializer = MusicSerializer(music)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        token = getBearerToken(request)
        print(token)
        payload = decode_jwt(token)
        user_id = payload.get("id")
        print("user id: ", user_id)
        music = self.get_object(pk)
        serializer = MusicSerializer(music, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        music_data = serializer.validated_data
        title = music_data.get("title", music.get("title"))
        album_name = music_data.get("album_name", music.get("album_name"))
        genre = music_data.get("genre", music.get("genre"))

        updated_music = updateMusic(title=title, album_name=album_name, genre=genre, pk=pk, userId=user_id)
        if not updated_music:
            return Response(
                {"detail": "Music not found"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = MusicSerializer(data=updated_music)
        serializer.is_valid()
        return Response(serializer.data)

    def delete(self, request, pk, format=None):
        try:
            deleteMusic(pk)
            return Response(
                {"message": "Profile deleted successfully!"},
                status=status.HTTP_204_NO_CONTENT,
            )
        except Exception as e:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
