from django.db import connection


def getAllMusic():
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM core_music")
        columns = [col[0] for col in cursor.description]
        music = [dict(zip(columns, row)) for row in cursor.fetchall()]
        print(music)
    return music


def getMusic(pk: int):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FOM core_music WHERE id = %s", (pk,))
        columns = [col[0] for col in cursor.description]
        row = cursor.fetchone()
        if row:
            return dict(zip(columns, row))
        return None
