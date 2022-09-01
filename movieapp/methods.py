from .models import *
from .serializers import *
from rest_framework.response import Response
import jwt
from rest_framework import status
from movie import settings
from rest_framework.exceptions import NotAuthenticated, AuthenticationFailed, NotFound


def CheckUser(token):
    if len(token) == 0 :
        raise NotAuthenticated
    try:
        tokenData = jwt.decode(token,settings.JWT_AUTH['JWT_SECRET_KEY'],algorithms=['HS256'])
        userid = tokenData['id']
    except:
        raise AuthenticationFailed
    try: 
        user = User.objects.get(id=userid)
        return user
    except:
        raise NotFound

