from django.shortcuts import render

from core.models import Music
from .serializers import MusicSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .selectors import getMusic, getAllMusic
from .services import createMusic, updateMusic, deleteMusic


class MusicList(APIView):
    def get(self, request, format=None):
        music = getAllMusic()
        serializer = MusicSerializer(music, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = MusicSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        music_data = serializer.validated_data
        music = createMusic(
            music_data["artist_id"],
            music_data["title"],
            music_data["albumn_name"],
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
        music = self.get_object(pk)
        serializer = MusicSerializer(music, data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        author_id = serializer.validated_data["author_id"]
        title = serializer.validated_data["title"]
        albumn_name = serializer.validated_data["albumn_name"]
        genre = serializer.validated_data["genre"]
        updated_music = updateMusic(
            pk, author_id=author_id, title=title, albumn_name=albumn_name, genre=genre
        )
        if not updated_music:
            return Response(
                {"detail": "Music not found"}, status=status.HTTP_404_NOT_FOUND
            )
        return Response(updated_music)

    def delete(self, request, pk, format=None):
        try:
            deleteMusic(pk)
            return Response(
                {"message": "Profile deleted successfully!"},
                status=status.HTTP_204_NO_CONTENT,
            )
        except Exception as e:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
