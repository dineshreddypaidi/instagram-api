from users import models as usermodels
from . import serializers
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate,logout,login
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404        

class Loginview(APIView):
    permission_classes = [AllowAny] 
    
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        
        if user:
            token, created = Token.objects.get_or_create(user=user)
            login(request,user)
            return Response({
                'token': token.key
                },status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
                           
class Registerview(APIView):
    permission_classes = [AllowAny] 
    
    def post(self, request):
        serializer = serializers.UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
             "message" : "user register succesfully",   
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class Logoutview(APIView):
    def post(self,request):
        token = Token.objects.get(user=request.user)
        token.delete()
        logout(request)
        return Response({"message": "Successfully logged out."}, status=status.HTTP_200_OK)
    
            
class logged_User(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            serializer = serializers.loggeduserserialzer(request.user)
            token, created = Token.objects.get_or_create(user=request.user)
            return Response({
                'user_data' : serializer.data,
                'token' : token.key,
                },status=status.HTTP_200_OK)
        else:
            return Response({
                "message": "User not logged in",
                }, status=status.HTTP_401_UNAUTHORIZED)
         
class postview(APIView):
    def get(self,request):
        user = request.user
        posts = usermodels.Post.objects.filter(user_id=user)
        serializer = serializers.Postserailizer(posts, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def post(self,request):
        serializer = serializers.Postserailizer(data=request.data)
        if serializer.is_valid():
            post = serializer.save(user=request.user)
            return Response(serializers.Postserailizer(post).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#user views to all
class Userview(APIView):
    permission_classes = [AllowAny] 

    def get(self, request, username):
        user = get_object_or_404(usermodels.CustomUser, username=username)
        serializer = serializers.UserviewSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class Userviewposts(APIView):
    permission_classes = [AllowAny]
    
    def get(self,request,username):
        try:
            user = usermodels.CustomUser.objects.get(username=username)
        except usermodels.CustomUser.DoesNotExist:
            return Response({"message": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        current_user = request.user
        if user.account_type == 'private':
            if current_user.is_authenticated:
                if usermodels.Follows.objects.filter(follower=current_user, following=user).exists():
                    posts = usermodels.Post.objects.filter( user=user)
                else:
                    return Response({"detail": "You do not have access to this user's posts."}, status=status.HTTP_403_FORBIDDEN)  
            else:
                return Response({'message':"not authenticated"},status=status.HTTP_403_FORBIDDEN)
        else:
            posts = usermodels.Post.objects.filter(user__account_type='public', user=user)
            
        if posts.exists():
            return Response(serializers.UserPostviewserailizer(posts, many=True).data, status=status.HTTP_200_OK) 
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)
        
class Postlikeview(APIView):
    def get(self, request,post_id):
        try:
            post = usermodels.Post.objects.get(post_id=post_id)
        except usermodels.Post.DoesNotExist:
            return Response({"message": "Post does not exist."}, status=status.HTTP_404_NOT_FOUND) 
        likes = usermodels.Postlikes.objects.filter(post_id=post)
        return Response(serializers.Postlikeserailizer(likes,many=True).data, status=status.HTTP_200_OK)
        
    def post(self,request,post_id):
        try:
            post = usermodels.Post.objects.get(post_id=post_id)
        except usermodels.Post.DoesNotExist:
            return Response({"message": "Post does not exist."}, status=status.HTTP_404_NOT_FOUND)
        data = {'post_id' : post.post_id,
                'user_id' : request.user.id} 
        try:
            like = usermodels.Postlikes.objects.get(post_id=post, user_id=request.user)
            return Response({"message": "already liked"}, status=status.HTTP_202_ACCEPTED)
        except usermodels.Postlikes.DoesNotExist:
            serializer =  serializers.Postlikeserailizer(data=data)
            
        if serializer.is_valid():
            like = serializer.save()
            return Response(serializers.Postlikeserailizer(like).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,post_id):
        try:
            post = usermodels.Post.objects.get(post_id=post_id)
        except usermodels.Post.DoesNotExist:
            return Response({"message": "Post does not exist."}, status=status.HTTP_404_NOT_FOUND)
        data = {'post_id' : post.post_id,
                'user_id' : request.user.id}
        try:
            like = usermodels.Postlikes.objects.get(post_id=post, user_id=request.user)
        except usermodels.Postlikes.DoesNotExist:
            return Response({"message": "like doesnot exist"}, status=status.HTTP_404_NOT_FOUND)
        like.delete()
        return Response({"message": "unliked"},status=status.HTTP_204_NO_CONTENT)

class Postcommentview(APIView):
    def get(self, request,post_id):
        try:
            post = usermodels.Post.objects.get(post_id=post_id)
        except usermodels.Post.DoesNotExist:
            return Response({"message": "Post does not exist."}, status=status.HTTP_404_NOT_FOUND) 
        likes = usermodels.Postcomment.objects.filter(post_id=post)
        return Response(serializers.Postcommentserailizer(likes,many=True).data, status=status.HTTP_200_OK)
        
    def post(self,request,post_id):
        try:
            post = usermodels.Post.objects.get(post_id=post_id)
        except usermodels.Post.DoesNotExist:
            return Response({"message": "Post does not exist."}, status=status.HTTP_404_NOT_FOUND)
        data = {'post_id' : post.post_id,
                'user_id' : request.user.id} | request.data
        serializer =  serializers.Postcommentserailizer(data=data)
        if serializer.is_valid():
            like = serializer.save()
            return Response(serializers.Postcommentserailizer(like).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, post_id):
        try:
            post = usermodels.Post.objects.get(post_id=post_id)
        except usermodels.Post.DoesNotExist:
            return Response({"message": "Post does not exist."}, status=status.HTTP_404_NOT_FOUND)
        
        comment_id = request.data.get('comment_id')
        if not comment_id:
            return Response({"message": "Comment ID is required."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            comment = usermodels.Postcomment.objects.get(id=comment_id, post_id=post, user_id=request.user)
        except usermodels.Postcomment.DoesNotExist:
            return Response({"message": "Comment does not exist."}, status=status.HTTP_404_NOT_FOUND)
        data = {'post_id': post.post_id, 'user_id': request.user.id} | request.data
        
        serializer = serializers.Postcommentserailizer(comment, data=data, partial=True)
        
        if serializer.is_valid():
            updated_comment = serializer.save()
            return Response(serializers.Postcommentserailizer(updated_comment).data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,post_id):
        try:
            post = usermodels.Post.objects.get(post_id=post_id)
        except usermodels.Post.DoesNotExist:
            return Response({"message": "Post does not exist."}, status=status.HTTP_404_NOT_FOUND)
        
        comment_id = request.data.get('comment_id')
        if not comment_id:
            return Response({"message": "Comment ID is required."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            comment = usermodels.Postcomment.objects.get(id=comment_id, post_id=post, user_id=request.user)
        except usermodels.Postcomment.DoesNotExist:
            return Response({"message": "Comment does not exist."}, status=status.HTTP_404_NOT_FOUND)
        comment.delete()
        return Response({"message": "Comment deleted"}, status=status.HTTP_204_NO_CONTENT)