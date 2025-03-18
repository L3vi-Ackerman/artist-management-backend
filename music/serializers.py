from asyncio import wait
from rest_framework import serializers
from django.utils import timezone
from core.models import Artist, Music
from django.contrib.auth import authenticate
from artist.serializers import ArtistSerializer


class MusicSerializer(serializers.Serializer):
    artist = ArtistSerializer(read_only=True)
    artist_id = serializers.PrimaryKeyRelatedField(
        queryset=Artist.objects.all(), many=True
    )
    title = serializers.CharField(max_length=255)
    albumn_name = serializers.CharField(max_length=255)
    genre = serializers.ChoiceField(choices=Music.GENRE)

    def create(self, validated_data):
        return Music.objects.create(**validated_data)

    def update(self, instance, validated_data):
        if "artist_id" in validated_data:
            instance.artist_id.set(validated_data["artist_id"])
        instance.title = validated_data.get("title", instance.title)
        instance.albumn_name = validated_data.get("albumn_name", instance.albumn_name)
        instance.genre = validated_data.get("genre", instance.genre)
        instance.save()
        return instance
