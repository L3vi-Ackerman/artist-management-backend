from django.db import connection
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from django.contrib.auth.hashers import check_password


def createUser(email: str, password: str, role: str):
    hashed_password = make_password(password)
    with connection.cursor() as cursor:
        cursor.execute(
            "INSERT INTO core_customuser (email,password,role,is_superuser, is_staff, is_active, date_joined) VALUES (%s, %s, %s,%s,%s, %s, %s) RETURNING ID",
            (email, hashed_password, role, False, False, True, timezone.now()),
        )
        user_id = cursor.fetchone()[0]
    return {"id": user_id, "email": email, "role": role}


def updateUser(pk, email, password, role):
    with connection.cursor() as cursor:
        cursor.execute(
            "UPDATE core_customuser SET email = %s, password = %s, role = %s, is_superuser = %s, is_staff = %s, is_active = %s WHERE id = %s RETURNING id, email, password, role",
            [email, password, role, False, False, True, pk],
        )
        updated_user = cursor.fetchone()
        if not updated_user:
            return None
        return {
            "id": updated_user[0],
            "email": updated_user[1],
            "password": updated_user[2],
        }


def deleteUser(pk):
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM core_customuser WHERE id = %s", [pk])


def loginUser(email, password):
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT id, email,password, role, is_active,is_staff,is_superuser FROM core_customuser WHERE email = %s",
            [email],
        )
        result = cursor.fetchone()
        print(f"result: ", result)
        if result:

            id, email, db_password, role, is_active, is_staff, is_superuser = result

            if check_password(password, db_password):
                print(f"password: ", password)
                print(f"db_password", db_password)
                user = {"id": id, "email": email, "is_active": is_active, "role": role}
                return user
        return None
