from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid

class CustomUser(AbstractUser):
    bio = models.TextField(blank=True, null=True)
    profile_image_url = models.URLField(blank=True, null=True)
    website_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    followers = models.PositiveIntegerField(blank=True,null=True)
    following = models.PositiveBigIntegerField(blank=True,null=True)
    posts = models.PositiveSmallIntegerField(blank=True,null=True)
    
    def __str__(self):
        return self.username
    
class Post(models.Model):
    post_id = models.UUIDField(default=uuid.uuid1, editable=False, unique=True)
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    content_url = models.URLField()
    caption = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.PositiveIntegerField(default=0)
    comments = models.PositiveIntegerField(default=0)
    shares = models.PositiveIntegerField(default=0)
    hashtags = models.TextField()
    
    def __str__(self) -> str:
        return f'{self.post_id} {self.user}'
    
class Postlikes(models.Model):
    like_id = models.UUIDField(default=uuid.uuid1, editable=False, unique=True)
    post_id = models.ForeignKey(Post,on_delete=models.CASCADE)
    user_id = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return self.post_id
    
class Postcomment(models.Model):
    comment_id = models.UUIDField(default=uuid.uuid1, editable=False, unique=True)
    post_id = models.ForeignKey(Post,on_delete=models.CASCADE)
    user_id = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return self.post_id  
    
class Follows(models.Model):
    follower = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="follower")
    following = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return self.follower.username