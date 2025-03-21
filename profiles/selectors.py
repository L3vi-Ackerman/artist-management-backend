from django.db import connection


def getAllProfiles():
    with connection.cursor() as cursor:
        cursor.execute(
            """SELECT core_customuser.email, 
            core_customuser.role, 
            core_profile.first_name, 
            core_profile.last_name, 
            core_profile.phone, 
            core_profile.dob, 
            core_profile.address, 
            core_profile.created_at 
            FROM core_profile JOIN core_customuser ON 
            core_profile.user_id = core_customuser.id"""
        )
        columns = [col[0] for col in cursor.description]
        profile = [dict(zip(columns, row)) for row in cursor.fetchall()]
        print(profile)
    return profile


def getProfile(pk: int):
    print("Primary Key: ", pk)
    with connection.cursor() as cursor:
        cursor.execute(
            """SELECT 
    core_customuser.email, 
    core_customuser.role, 
    core_profile.first_name, 
    core_profile.last_name, 
    core_profile.phone, 
    core_profile.dob, 
    core_profile.address, 
    core_profile.created_at 
FROM core_profile 
JOIN core_customuser ON core_profile.user_id = core_customuser.id 
WHERE core_profile.id = %s
""",
            (pk,),
        )
        columns = [col[0] for col in cursor.description]
        row = cursor.fetchone()

        if row:
            return dict(zip(columns, row))
        return None
