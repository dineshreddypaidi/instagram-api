from users import models as usermodels
from . import serializers
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

class Users(APIView):
    def get(self, request):
        users = usermodels.CustomUser.objects.all()
        serializer = serializers.UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = serializers.UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class logged_User(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            serializer = serializers.UserSerializer(request.user)
            return Response(serializer.data)
        else:
            return Response({
                "message": "User not logged in",
                "status" : "401",
                }, status=status.HTTP_401_UNAUTHORIZED)
            