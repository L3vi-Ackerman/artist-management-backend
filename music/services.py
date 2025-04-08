from django.db import connection
from django.utils import timezone


def createMusic(artist_id, title, album_name, genre):

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                    "INSERT INTO core_music (artist_id, title, album_name, genre, created_at, updated_at) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id;",
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


def updateMusic(title, album_name, genre, pk: int = None, userId: int = None):
    try:
        if not pk or not userId:
            raise ValueError("Both pk (music ID) and userId must be provided")
        with connection.cursor() as cursor:
            cursor.execute("SELECT core_music.artist_id from core_music where id = %s", (pk,))
            artist_id = cursor.fetchone()
            print("from first raw query artist_id: ", artist_id)
        with connection.cursor() as cursor:
            cursor.execute(
            """
                SELECT core_artist.id from core_artist where manager_id = (
                SELECT manager_id from core_artist where user_id  = %s)
                """,(userId,)
            )
            artist_second_id = cursor.fetchone()

            if artist_second_id:
                artist_second_id = artist_second_id[0]
                print("from second raw query: artist_id: ", artist_second_id)
            else:
                print("No artist found.")
            print("from second raw query: artist_id: ", artist_second_id )
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT core_music.id
                FROM core_music 
                WHERE core_music.id = %s
                  AND (core_music.artist_id = (SELECT core_artist.id FROM core_artist WHERE core_artist.user_id = %s)
                        OR c.artist_id IN (SELECT id
                        FROM core_artist
                        WHERE manager_id = (SELECT manager_id
                        FROM core_artist
                        WHERE user_id = %s)))
            """, [pk, userId, userId])
            permission = cursor.fetchone()
            print("permission: ",permission)

        if not permission:
            print(f"Unauthorized update attempt for music ID: {pk} by user ID: {userId}")
            return None

        with connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE core_music
                SET title = %s, album_name = %s, genre = %s, updated_at = %s
                WHERE id = %s
                RETURNING id, artist_id, title, album_name, genre, created_at, updated_at;
                """,
                [title, album_name, genre, timezone.now(), pk],
            )
            updated_music = cursor.fetchone()
            if updated_music:
                columns = [col[0] for col in cursor.description]
                return dict(zip(columns, updated_music))
            return None

    except ValueError as e:
        print(f"Error: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
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
