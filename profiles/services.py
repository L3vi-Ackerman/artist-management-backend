from django.db import connection
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from django.contrib.auth.hashers import check_password


def createProfile(userId:int, first_name:str="", last_name="", phone=None, dob=None, address=""):
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
            "created_at":timezone.now(),
            "updated_at":timezone.now()
            }

def updateProfile(first_name, last_name, phone, dob, address, pk: int = None, userId: int = None):
    if pk:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE core_profile SET
                first_name = %s,
                last_name = %s,
                phone = %s,
                dob = %s,
                address = %s,
                updated_at = %s
                WHERE id = %s
                RETURNING
                id, first_name, last_name, phone, dob, address, updated_at
                """,
                [first_name, last_name, phone, dob, address, timezone.now(), pk],
            )

            updated_profile = cursor.fetchone()
            # print(updated_profile) # Remove or comment out in production
            if not updated_profile:
                return None
            return {
                "id": updated_profile[0],
                "first_name": updated_profile[1],
                "last_name": updated_profile[2],
                "phone": updated_profile[3],
                "dob": updated_profile[4],
                "address": updated_profile[5],
                "updated_at": updated_profile[6],
            }
    elif userId:  # Added elif to make the logic clearer
        with connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE core_profile SET
                first_name = %s,
                last_name = %s,
                phone = %s,
                dob = %s,
                address = %s,
                updated_at = %s
                WHERE id = %s
                RETURNING
                id, first_name, last_name, phone, dob, address, updated_at""",
                [first_name, last_name, phone, dob, address, timezone.now(), userId],
            )

            updated_profile = cursor.fetchone()
            if not updated_profile:
                return None
            return {
                "id": updated_profile[0],
                "first_name": updated_profile[1],
                "last_name": updated_profile[2],
                "phone": updated_profile[3],
                "dob": updated_profile[4],
                "address": updated_profile[5],
                "updated_at": updated_profile[6],
            }
    else:
        return None  # Or raise an error indicating that either pk or userId is required
def deleteProfile(pk):
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM core_profile WHERE id = %s", [pk])
