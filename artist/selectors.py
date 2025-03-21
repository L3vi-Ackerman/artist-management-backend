from django.core.paginator import Paginator
from django.db import connection
from core.models import Artist


def get_paginated_artists(request, paginator):
    with connection.cursor() as cursor:
        cursor.execute(
            """
         SELECT      
         core_customuser.id,        
         core_customuser.email,
         core_customuser.role,
         core_artist.name,
         core_artist.dob,
         core_artist.gender,
         core_artist.address,
         core_artist.first_release_year,
         core_artist.no_of_albumns_released,
         core_artist.created_at,
         core_artist.updated_at
         FROM core_artist JOIN core_customuser 
         ON core_artist.user_id = core_customuser.id
        """
        )
        columns = [col[0] for col in cursor.description]
        artists_dicts = [dict(zip(columns, row)) for row in cursor.fetchall()]
        print(cursor.fetchall())

    if not artists_dicts:
        return paginator.get_paginated_response([])

    artist_instances = [
        Artist(
            user_id=artist_dict["id"],
            email=artist_dict["email"],
            role=artist_dict["role"],
            name=artist_dict["name"],
            dob=artist_dict["dob"],
            gender=artist_dict["gender"],
            address=artist_dict["address"],
            first_release_year=artist_dict["first_release_year"],
            no_of_albumns_released=artist_dict["no_of_albumns_released"],
            created_at=artist_dict["created_at"],
            updated_at=artist_dict["updated_at"],
        )
        for artist_dict in artists_dicts
    ]

    # Returning the paginated response
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
