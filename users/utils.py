import jwt
import datetime
from django.conf import settings
from rest_framework.authentication import BaseAuthentication

SECRET_KEY = settings.SECRET_KEY


def create_jwt(user):
    accessPayload = {
        "id": user["id"],
        "email": user["email"],
        "role": user["role"],
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=15),
        "iat": datetime.datetime.utcnow(),
    }

    accessToken = jwt.encode(accessPayload, SECRET_KEY, algorithm="HS256")

    refreshPayload = {
        "id": user["id"],
        "email": user["email"],
        "role": user["role"],
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=15),
        "iat": datetime.datetime.utcnow(),
    }

    refreshToken = jwt.encode(refreshPayload, SECRET_KEY, algorithm="HS256")

    return {"accessToken": accessToken, "refreshToken": refreshToken}


def decode_jwt(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        return {"error": "Token has Expired"}
    except jwt.InvalidTokenError:
        return {"error": "Invalid Token"}
