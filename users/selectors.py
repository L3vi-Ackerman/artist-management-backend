from django.db import connection


def getAllUsers():
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM core_customuser")
        columns = [col[0] for col in cursor.description]
        users = [dict(zip(columns, row)) for row in cursor.fetchall()]
    return users


def getUser(pk: int):
    print("Primary Key: ", pk)
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM core_customuser WHERE id = %s", (pk,))
        columns = [col[0] for col in cursor.description]
        row = cursor.fetchone()

        if row:
            return dict(zip(columns, row))
        return None
