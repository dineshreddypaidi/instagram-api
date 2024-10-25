from rest_framework.response import Response
from rest_framework.views import APIView
from users import models as usermodels
from . import serializers
from rest_framework import viewsets

class Users(viewsets.ModelViewSet):
    queryset =usermodels.CustomUser.objects.all()
    serializer_class = serializers.UserSerializer
    
    