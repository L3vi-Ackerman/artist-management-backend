from django.db import connection
from django.contrib.auth.hashers import make_password
from django.utils import timezone


def createUser(email: str, password: str, role: str):
    hashed_password = make_password(password)
    with connection.cursor() as cursor:
        cursor.execute(
            "INSERT INTO core_customuser (email,password,role,is_superuser, is_staff, is_active, date_joined) VALUES (%s, %s, %s,%s,%s, %s, %s) RETURNING ID",
            (email, hashed_password, role, False, False, True, timezone.now()),
        )
        user_id = cursor.fetchone()[0]
    return {"id": user_id, "email": email, "role": role}


def deleteUser(pk):
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM core_customuser WHERE id = %s", [pk])
