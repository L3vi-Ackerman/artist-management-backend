from django.db import connection

from django.db import connection

from django.db import connection

def getAllMusic():
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT
                cm.id AS music_id,
                cm.title,
                cm.album_name,
                cm.genre,
                cm.created_at AS music_created_at,
                cm.updated_at AS music_updated_at,
                ca.id AS artist_id,
                ca.name AS artist_name,
                ca.dob AS artist_dob,
                ca.gender AS artist_gender,
                ca.address AS artist_address,
                ca.first_release_year AS artist_first_release_year,
                ca.no_of_albumns_released AS artist_no_of_albumns_released,
                ca.created_at AS artist_created_at,
                ca.updated_at AS artist_updated_at
            FROM core_music cm
            JOIN core_artist ca ON cm.artist_id = ca.id"""
        )
        columns = [col[0] for col in cursor.description]
        music_data = [dict(zip(columns, row)) for row in cursor.fetchall()]
        print(music_data)
        return music_data
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
