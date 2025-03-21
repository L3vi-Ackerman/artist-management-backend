from django.db import connection

from django.db import connection


def getAllMusic():
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT 
                core_music.id,
                core_music.title,
                core_music.albumn_name,
                core_music.genre,
                core_music.created_at,
                core_music.updated_at,
                core_artist.id as artist_id,
                core_artist.name as artist_name 
            FROM core_music
            JOIN core_artist ON core_music.artist_id = core_artist.id;
        """
        )
        columns = [col[0] for col in cursor.description]
        music = [dict(zip(columns, row)) for row in cursor.fetchall()]
        return music


def getMusic(pk: int):
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT 
                core_music.id,
                core_music.title,
                core_music.albumn_name,
                core_music.genre,
                core_music.created_at,
                core_music.updated_at,
                core_artist.id as artist_id,
                core_artist.name as artist_name 
            FROM core_music
            JOIN core_artist ON core_music.artist_id = core_artist.id
            WHERE core_music.id = %s;
        """,
            [pk],
        )
        columns = [col[0] for col in cursor.description]
        row = cursor.fetchone()
        if row:
            return dict(zip(columns, row))
        return None
