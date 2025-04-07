from django.core.paginator import Paginator
from django.db import connection
from core.models import Artist,Profile


def get_paginated_artists(request, paginator, userID:int):
    print('user id is: ', userID)
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT * FROM core_artist
            WHERE core_artist.manager_id = (
            SELECT id from core_profile
            WHERE core_profile.user_id = %s
    )
                       """,[userID])
        
        columns = [col[0] for col in cursor.description]
        artists_dicts = [dict(zip(columns, row)) for row in cursor.fetchall()]

    artist_instances = []
    for artist_dict in artists_dicts:
        manager_id = artist_dict.get('manager_id')
        manager_instance = None
        if manager_id:
            try:
                manager_instance = Profile.objects.get(pk=manager_id)
            except Profile.DoesNotExist:
                print(f"Warning: Profile with ID {manager_id} not found.")
        artist_instance = Artist(
                id=artist_dict["id"],
                user_id=artist_dict["user_id"],
                name=artist_dict["name"],
                dob=artist_dict["dob"],
                manager=manager_instance,
                gender=artist_dict["gender"],
                address=artist_dict["address"],
                first_release_year=artist_dict["first_release_year"],
                no_of_albumns_released=artist_dict["no_of_albumns_released"],
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

def getSingleArtist(userId:int):
    print(userId)
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM core_artist WHERE user_id = %s", (userId,))
        columns = [col[0] for col in cursor.description]
        row = cursor.fetchone()
        print(row)
        if row:
            return dict(zip(columns, row))
    return None
