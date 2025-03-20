from rest_framework import serializers
from core.models import Artist, Music
from artist.serializers import ArtistSerializer


class MusicSerializer(serializers.Serializer):

    artist_id = serializers.IntegerField()
    title = serializers.CharField(max_length=255)
    albumn_name = serializers.CharField(max_length=255)
    genre = serializers.ChoiceField(choices=Music.GENRE)
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()

    def create(self, validated_data):
        artist_id = validated_data.pop("artist_id")
        artist = Artist.objects.get(pk=artist_id)
        return Music.objects.create(artist_id=artist, **validated_data)

    def update(self, instance, validated_data):
        artist_id = validated_data.pop("artist_id")
        artist = Artist.objects.get(pk=artist_id)
        instance.artist_id = artist
        instance.title = validated_data.get("title", instance.title)
        instance.album_name = validated_data.get("albumn_name", instance.album_name)
        instance.genre = validated_data.get("genre", instance.genre)
        instance.save()
        return instance
