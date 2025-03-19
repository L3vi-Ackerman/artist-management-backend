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
