import json

from django.shortcuts import render
from django.conf import settings
from django.contrib.auth import get_user_model
from .serializers import  AppTokenSerializer
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.middleware.csrf import get_token
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework_simplejwt import views as jwt_views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)

User = get_user_model()



@api_view(['GET'])
@ensure_csrf_cookie
def get_csrf_token(request):
    # 前后端分离业务
    token = get_token(request)
    return Response({'csrf_token': token})


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = AppTokenSerializer


