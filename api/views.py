from users import models as usermodels
from . import serializers
from rest_framework import viewsets,status
from rest_framework.views import APIView
from rest_framework.response import Response

class Users(viewsets.ModelViewSet):
    queryset =usermodels.CustomUser.objects.all()
    serializer_class = serializers.UserSerializer
    lookup_field = 'username'

class User(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            serializer = serializers.UserSerializer(request.user)
            return Response(serializer.data)
        else:
            return Response({
                "message": "User not logged in",
                "status" : "401",
                }, status=status.HTTP_401_UNAUTHORIZED)
            
    def post(self,request):        
        pass
