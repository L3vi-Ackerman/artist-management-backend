from rest_framework import serializers
from core.models import Artist, Music
from artist.serializers import ArtistSerializer


class MusicSerializer(serializers.Serializer):

    id = serializers.IntegerField(read_only=True)
    # artist_id = serializers.IntegerField()
    artist = ArtistSerializer(read_only=True) 
    title = serializers.CharField(max_length=255, required=False,allow_null=True)
    album_name = serializers.CharField(max_length=255,required=False, allow_null=True)
    genre = serializers.ChoiceField(choices=Music.GENRE,required=False,allow_null=True)
    # created_at = serializers.DateTimeField()
    # updated_at = serializers.DateTimeField()

   
