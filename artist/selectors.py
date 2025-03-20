from django.core.paginator import Paginator
from django.db import connection
from core.models import Artist


def get_paginated_artists(request, paginator):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM core_artist")
        columns = [col[0] for col in cursor.description]
        artists_dicts = [dict(zip(columns, row)) for row in cursor.fetchall()]
        print("Artist Id: ", artists_dicts[0]["id"])

    artist_instances = []
    for artist_dict in artists_dicts:
        artist_instance = Artist(
            id=artist_dict["id"],
            user_id=artist_dict["user_id"],
            name=artist_dict["name"],
            dob=artist_dict["dob"],
            gender=artist_dict["gender"],
            address=artist_dict["address"],
            first_release_year=artist_dict["first_release_year"],
            no_of_albumns_released=artist_dict["no_of_albumns_released"],
            created_at=artist_dict["created_at"],
            updated_at=artist_dict["updated_at"],
        )
        print(repr(artist_instance))
        artist_instances.append(artist_instance)

    return paginator.paginate_queryset(artist_instances, request)


def getArtist(pk: int):
    print(pk)
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM core_artist WHERE id = %s", (pk,))
        columns = [col[0] for col in cursor.description]
        row = cursor.fetchone()
        print(row)
        if row:
            return dict(zip(columns, row))
        return None
