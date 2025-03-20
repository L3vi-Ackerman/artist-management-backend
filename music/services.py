from django.db import connection
from django.utils import timezone


def createMusic(artist_id, title, album_name, genre):

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO core_music (artist_id, title, albumn_name, genre, created_at, updated_at) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id;",
                [artist_id, title, album_name, genre, timezone.now(), timezone.now()],
            )

            music_id = cursor.fetchone()[0]
            print(music_id)
            return {
                "id": music_id,
                "artist_id": artist_id,
                "title": title,
                "album_name": album_name,
                "genre": genre,
                "created_at": timezone.now(),
                "updated_at": timezone.now(),
            }

    except Exception as e:
        print(f"Error creating music: {e}")
        return None


def updateMusic(pk, title, album_name, genre):
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE core_music
                SET title = %s, albumn_name = %s, genre = %s, updated_at = %s
                WHERE id = %s
                RETURNING id, artist_id, title, albumn_name, genre, created_at, updated_at;
                """,
                [title, album_name, genre, timezone.now(), pk],
            )
            updated_music = cursor.fetchone()
            if updated_music:
                columns = [col[0] for col in cursor.description]
                return dict(zip(columns, updated_music))
            return None

    except Exception as e:
        print(f"Error updating music: {e}")
        return None


def deleteMusic(pk):
    """Deletes a Music record using a raw SQL query."""
    try:
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM core_music WHERE id = %s;", [pk])
            return True
    except Exception as e:
        print(f"Error deleting music: {e}")
        return False
