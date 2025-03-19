from django.db import connection
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from django.contrib.auth.hashers import check_password


def createArtist(
    userId: int, dob: str, gender: str, release_year: int, no_of_albumns: int
):
    with connection.cursor() as cursor:
        cursor.execute(
            "INSERT INTO core_artist (user_id,dob,gender,first_release_year,no_of_albumns_released,created_at,updated_at) VALUES (%s, %s,%s,%s,%s,%s,%s) RETURNING ID",
            (
                userId,
                dob,
                gender,
                release_year,
                no_of_albumns,
                timezone.now(),
                timezone.now(),
            ),
        )
        newArtist = cursor.fetchone()
        print(f"newArtist: ", newArtist[0])
    return {
        "id": newArtist[0],
        "dob": dob,
        "gender": gender,
        "first_release_year": release_year,
        "no_of_albumns_released": no_of_albumns,
        "created_at": timezone.now(),
        "updated_at": timezone.now(),
    }


def updateArtist(pk, dob, gender, first_release_year, no_of_albumns_released):

    with connection.cursor() as cursor:
        cursor.execute(
            "UPDATE core_artist SET dob = %s, gender = %s, first_release_year = %s, no_of_albumns_released = %s WHERE id = %s RETURNING id, dob, gender, first_release_year,no_of_albumns_released",
            [dob, gender, first_release_year, no_of_albumns_released, pk],
        )

        updated_artist = cursor.fetchone()
        print(updated_artist)
        if not updated_artist:
            return None
        return {
            "id": updated_artist[0],
            "dob": updated_artist[1],
            "gender": updated_artist[2],
            "first_release_year": updated_artist[3],
            "no_of_albumns_released": updated_artist[4],
        }


def deleteArtist(pk):
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM core_artist WHERE id = %s", [pk])
