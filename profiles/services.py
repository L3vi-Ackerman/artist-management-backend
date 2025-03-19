from django.db import connection
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from django.contrib.auth.hashers import check_password


def createProfile(userId, first_name, last_name, phone, dob, address):
    with connection.cursor() as cursor:
        cursor.execute(
            "INSERT INTO core_profile (user_id, first_name,last_name,phone, dob,address, created_at, updated_at) VALUES (%s,%s,%s,%s,%s,%s, %s, %s) RETURNING ID",
            (
                userId,
                first_name,
                last_name,
                phone,
                dob,
                address,
                timezone.now(),
                timezone.now(),
            ),
        )
        newProfile = cursor.fetchone()
        print(f"newProfile: ", newProfile)

    return {
        "id": newProfile[0],
        "first_name": first_name,
        "last_name": last_name,
        "phone": phone,
        "dob": dob,
        "address": address,
    }


def updateProfile(pk, first_name, last_name, phone, dob, address):

    with connection.cursor() as cursor:
        cursor.execute(
            "UPDATE core_artist SET first_name = %s, last_name = %s, phone = %s, dob = %s, address = %s WHERE id = %s RETURNING id, dob, gender, first_release_year,no_of_albumns_released",
            [first_name, last_name, phone, dob, address, pk],
        )

        updated_profile = cursor.fetchone()
        print(updated_profile)
        if not updated_profile:
            return None
        return {
            "id": updated_profile[0],
            "first_name": updated_profile[1],
            "last_name": updated_profile[2],
            "phone": updated_profile[3],
            "dob": updated_profile[4],
            "address": updated_profile[5],
        }
