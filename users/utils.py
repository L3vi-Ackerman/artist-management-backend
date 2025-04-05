import jwt
import datetime
from django.conf import settings
from rest_framework.authentication import BaseAuthentication

SECRET_KEY = settings.SECRET_KEY

def getBearerToken(request):
    authHeader = request.headers.get('Authorization')
    if authHeader:
        return authHeader.split(' ')[1]
    return None
def create_jwt(user):
    accessPayload = {
        "id": user["id"],  # Access id from the dict
        "email": user["email"], # Access email from the dict
        "role": user["role"], # Access role from the dict
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=15),
        "iat": datetime.datetime.utcnow(),
    }

    accessToken = jwt.encode(accessPayload, SECRET_KEY, algorithm="HS256")

    refreshPayload = {
        "id": user["id"], # Access id from the dict
        "email": user["email"], # Access email from the dict
        "role": user["role"], # Access role from the dict
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=7), # increased refresh token expiration.
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

def verify_refresh_token(refresh_token):
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=["HS256"])
        # You might want to add additional checks here,
        # such as verifying if the token is in a blacklist or has been used before
        return payload
    except jwt.ExpiredSignatureError:
        raise Exception("Refresh token has expired")
    except jwt.InvalidTokenError:
        raise Exception("Invalid refresh token")
