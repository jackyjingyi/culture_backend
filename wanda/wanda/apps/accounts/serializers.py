from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from datetime import datetime
from .models import User


class AppTokenSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['uname'] = user.name
        token['nbf'] = int(round(datetime.timestamp(datetime.now()), 0))
        token['org_exp'] = ''
        token['org_code'] = user.company.org_code if user.company else ''
        token['org_name'] = user.company.name if user.company else ''
        token['avatar'] = None
        token['super'] = 0
        token['is_senior'] = 0
        return token
