from django.db import connection
from core.models import Profile

def getAllProfiles():
    
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM core_profile")
        columns = [col[0] for col in cursor.description]
        profiles_data = cursor.fetchall()

        profiles = []
        for row in profiles_data:
            profile_dict = dict(zip(columns, row))
            profile = Profile(**profile_dict)
            profiles.append(profile)

        return profiles


def getProfile(pk: int):
    print(pk)
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM core_profile WHERE id = %s", (pk,))
        columns = [col[0] for col in cursor.description]
        row = cursor.fetchone()
        print(row)
        if row:
            return dict(zip(columns, row))
        return None
