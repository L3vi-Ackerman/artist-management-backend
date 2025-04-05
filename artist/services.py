from django.db import connection
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from django.contrib.auth.hashers import check_password


def createArtist(
        userId: int,
        name: str="",
        dob: str=None,
        gender: str="",
        address: str="",
        release_year: str="",
        no_of_albumns: int=None,
        ):
    with connection.cursor() as cursor:
        cursor.execute(
                "INSERT INTO core_artist (user_id,name, dob,gender,address, first_release_year,no_of_albumns_released,created_at, updated_at) VALUES (%s, %s,%s,%s,%s,%s,%s,%s,%s) RETURNING ID",
                (
                    userId,
                    name,
                    dob,
                    gender,
                    address,
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
            "name": name,
            "dob": dob,
            "gender": gender,
            "first_release_year": release_year,
            "no_of_albumns_released": no_of_albumns,
            "created_at": timezone.now(),
            "updated_at": timezone.now(),
            }


def updateArtist(
        name, dob, gender, address, first_release_year, no_of_albumns_released,pk:int=None,userId:int = None 
        ):
    print(f"name :", name)
    print(f"dob: ", dob)
    print(f"gender: ", gender)
    print(f"address: ", address)
    try:
        if pk:
            with connection.cursor() as cursor:
                cursor.execute(
                        "UPDATE core_artist SET name = %s, dob = %s, gender = %s, address = %s, first_release_year = %s, no_of_albumns_released = %s, updated_at = %s WHERE id = %s RETURNING id, name, dob, gender, address, first_release_year, no_of_albumns_released",
                        [
                            name,
                            dob,
                            gender,
                            address,
                            first_release_year,
                            no_of_albumns_released,
                            timezone.now(),
                            pk
                            ],
                        )

            updated_artist = cursor.fetchone()

            if not updated_artist:
                return None

            return {
                    "id": updated_artist[0],
                    "name": updated_artist[1],
                    "dob": updated_artist[2],
                    "gender": updated_artist[3],
                    "address": updated_artist[4],
                    "first_release_year": updated_artist[5],
                    "no_of_albumns_released": updated_artist[6],
                    }
        else:
            with connection.cursor() as cursor:
                cursor.execute(
                        "UPDATE core_artist SET name = %s, dob = %s, gender = %s, address = %s, first_release_year = %s, no_of_albumns_released = %s, updated_at = %s WHERE id = %s RETURNING id, name, dob, gender, address, first_release_year, no_of_albumns_released",
                        [
                            name,
                            dob,
                            gender,
                            address,
                            first_release_year,
                            no_of_albumns_released,
                            timezone.now(),
                            userId,
                            ],
                        )

            updated_artist = cursor.fetchone()

            if not updated_artist:
                return None

            return {
                    "id": updated_artist[0],
                    "name": updated_artist[1],
                    "dob": updated_artist[2],
                    "gender": updated_artist[3],
                    "address": updated_artist[4],
                    "first_release_year": updated_artist[5],
                    "no_of_albumns_released": updated_artist[6],
                    }
    except Exception as e:
        print(f"Error during update: {e}")
        return None


def deleteArtist(pk):
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM core_artist WHERE id = %s", [pk])
