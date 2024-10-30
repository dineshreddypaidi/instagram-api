from users import models as usermodels
from . import serializers
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate,logout,login
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404        
from django.db import transaction

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
        serializer = serializers.User_registerSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
             "message" : "user register succesfully",
             "user" : {
                 "id" : user.id,
                 "username" : user.username,
                 "name" : user.name,
                 "account_type" : user.account_type
                }
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
            serializer = serializers.UserSerializer(request.user)
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
        user = usermodels.CustomUser.objects.get(id=request.user.id)
        serializer = serializers.Postserailizer(data=request.data)
        if serializer.is_valid():
            with transaction.atomic():
                post = serializer.save(user=user)
                user.posts += 1
                user.save()
            return Response(serializers.Postserailizer(post).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class userfollowersview(APIView):
    def get(self,request):
        user = request.user
        followers = usermodels.Follows.objects.filter(following=user)
        follower_data = [{
            'id': f.follower.id,
            'username': f.follower.username,
            'name' : f.follower.name,
            'profile_img' : f.follower.profile_image_url} for f in followers]
        return Response(follower_data, status=status.HTTP_200_OK)
        
    def post(self,request):
        following_user = usermodels.CustomUser.objects.get(id=request.user.id)
        follower_id = request.data.get("id")
        
        try:
            follower_user = usermodels.CustomUser.objects.get(id=follower_id)
        except usermodels.CustomUser.DoesNotExist:
           return Response({'message': 'user does not exist'}, status=status.HTTP_404_NOT_FOUND)
       
        if following_user.id == follower_user.id:
            return Response({'message': 'you cant follow yourself'}, status=status.HTTP_400_BAD_REQUEST)
               
        if usermodels.Follows.objects.filter(follower=following_user, following=follower_user).exists():
            return Response({'message': 'You are already following this user'}, status=status.HTTP_400_BAD_REQUEST)
        
        data = {
            'follower' : following_user.id,
            'following': follower_user.id
            }
        
        serializer = serializers.userfollowserailizer(data=data)
        
        if serializer.is_valid():
            with transaction.atomic():
                serializer.save()
                follower_user.followers += 1
                follower_user.save()
                following_user.followings +=1
                following_user.save()
            return Response({'message':'follower added'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request):
        following_user = usermodels.CustomUser.objects.get(id=request.user.id)
        follower_id = request.data.get("id")
        
        try:
            follower_user = usermodels.CustomUser.objects.get(id=follower_id)
        except usermodels.CustomUser.DoesNotExist:
           return Response({'message': 'user does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
        if following_user.id == follower_user.id:
            return Response({'message': 'are you okay.?'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            deletethis = usermodels.Follows.objects.filter(follower=following_user, following=follower_user)
        except usermodels.Follows.DoesNotExist: 
            return Response({'message': 'You are not following'}, status=status.HTTP_400_BAD_REQUEST)
        
        with transaction.atomic():
                deletethis.delete()
                follower_user.followers -= 1
                follower_user.save()
                following_user.followings -=1
                following_user.save()
        return Response({'message': 'user unfollowed'}, status=status.HTTP_200_OK)
class userfolloweringview(APIView):
    def get(self,request):
        user = request.user
        following = usermodels.Follows.objects.filter(follower=user)
        follower_data = [{
            'id': f.follower.id,
            'username': f.follower.username,
            'name' : f.follower.name,
            'profile_img' : f.follower.profile_image_url} for f in following]
        return Response(follower_data, status=status.HTTP_202_ACCEPTED)
        
    def delete(self,request):
        following_user = request.data.get("id")
        follower_id = usermodels.CustomUser.objects.get(id=request.user.id)
         
        try:
            follower_user = usermodels.CustomUser.objects.get(id=follower_id)
        except usermodels.CustomUser.DoesNotExist:
           return Response({'message': 'user does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
        if following_user.id == follower_user.id:
            return Response({'message': 'are you okay.?'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            deletethis = usermodels.Follows.objects.filter(follower=following_user, following=follower_user)
        except usermodels.Follows.DoesNotExist: 
            return Response({'message': 'You are not following'}, status=status.HTTP_400_BAD_REQUEST)
        
        with transaction.atomic():
                deletethis.delete()
                follower_user.followers -= 1
                follower_user.save()
                following_user.followings -=1
                following_user.save()
        return Response({'message': 'user removed'}, status=status.HTTP_202_ACCEPTED)
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
            with transaction.atomic():
                like = serializer.save()
                post.likes += 1
                post.save()
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
            like = usermodels.Postlikes.objects.get(**data)
        except usermodels.Postlikes.DoesNotExist:
            return Response({"message": "like doesnot exist"}, status=status.HTTP_404_NOT_FOUND)
        with transaction.atomic():
            like.delete()
            post.likes -= 1
            post.save()
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
            with transaction.atomic():
                post.comments +=1 
                post.save()
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
        post.comments -= 1
        post.save()
        return Response({"message": "Comment deleted"}, status=status.HTTP_204_NO_CONTENT)
    

#user views to all
class Userview(APIView):
    permission_classes = [AllowAny] 

    def get(self, request, username):
        user = get_object_or_404(usermodels.CustomUser, username=username)
        serializer = serializers.UserSerializer(user)
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
            
class userviewfollowing(APIView):
    def get(self,request,username):
        try:
            user = usermodels.CustomUser.objects.get(username=username)
        except usermodels.CustomUser.DoesNotExist:
            return Response({"message": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        
        current_user = request.user
        
        if user.account_type == 'private':
            if current_user.is_authenticated:
                if usermodels.Follows.objects.filter(follower=current_user, following=user).exists():
                   following = usermodels.Follows.objects.filter(follower=user)
                else:
                    return Response({"detail": "You do not have access to this user's posts."}, status=status.HTTP_403_FORBIDDEN)  
            else:
                return Response({'message':"not authenticated"},status=status.HTTP_403_FORBIDDEN)
        else:
            following = usermodels.Follows.objects.filter(follower=user)
            
        follower_data = [{
            'id': f.follower.id,
            'username': f.follower.username,
            'name' : f.follower.name,
            'profile_img' : f.follower.profile_image_url} for f in following]
        return Response(follower_data, status=status.HTTP_200_OK)

class userviewfollower(APIView):
    def get(self,request,username):
        try:
            user = usermodels.CustomUser.objects.get(username=username)
        except usermodels.CustomUser.DoesNotExist:
            return Response({"message": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        
        followers = usermodels.Follows.objects.filter(following=user)
        follower_data = [{
            'id': f.follower.id,
            'username': f.follower.username,
            'name' : f.follower.name,
            'profile_img' : f.follower.profile_image_url} for f in followers]
        return Response(follower_data, status=status.HTTP_200_OK)
