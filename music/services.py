from django.db import connection
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from django.contrib.auth.hashers import check_password


def createMusic(artist_id, title, albumn_name, genre):
    with connection.cursor() as cursor:
        cursor.execute(
            "INSERT INTO core_music (artist_id, title, albumn_name, genre) VALUES (%s %s, %s, %s, %s) RETURNING ID",
            (artist_id, title, albumn_name, genre),
        )
        newMusic = cursor.fetchone()
        print(f"newMusicInstance: ", newMusic)

    return {
        "id": newMusic[0],
        "artist_id": artist_id,
        "title": title,
        "albumn_name": albumn_name,
        "genre": genre,
    }


def updateMusic(pk, title, albumn_name, genre):
    with connection.cursor() as cursor:
        cursor.execute(
            "UPDATE core_music SET title = %s, albumn_name=%s, genre=%s WHERE id = %s RETURNING id,title, albumn_name,genre",
            [title, albumn_name, genre, pk],
        )
        updated_music = cursor.fetchone()
        print(updated_music)
        if not updated_music:
            return None
        return {
            "id": updated_music[0],
            "title": updated_music[1],
            "albumn_name": updated_music[2],
            "genre": updated_music[3],
        }


def deleteMusic(pk):
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM core_music WHERE id = %s", [pk])
