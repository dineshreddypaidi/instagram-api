from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid,random,string

#for unique id genaration
def generate_id():
    while True:
        generated_id = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        if not Post.objects.filter(post_id=generated_id).exists():
            return generated_id
        
class CustomUser(AbstractUser):
    ACCOUNT_TYPE = [
        ('private', 'private'),
        ('public','public'),
    ]
    bio = models.TextField(blank=True, null=True)
    profile_image_url = models.URLField(blank=True, null=True)
    name = models.CharField(max_length=100)
    website_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    followers = models.PositiveIntegerField(default=0)
    followings = models.PositiveIntegerField(default=0)
    posts = models.PositiveIntegerField(default=0)
    account_type = models.CharField(max_length=10, choices=ACCOUNT_TYPE,default='public')
    
    def __str__(self):
        return self.username
    
class Post(models.Model):
    POST_TYPES = [
        ('reel', 'reel'),
        ('img', 'img'),
    ]
    post_id = models.CharField(max_length=11, primary_key=True, editable=False, default=generate_id)
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    content_url = models.URLField()
    caption = models.TextField()
    post_type = models.CharField(max_length=5, choices=POST_TYPES, default='img')
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.PositiveIntegerField(default=0)
    comments = models.PositiveIntegerField(default=0)
    shares = models.PositiveIntegerField(default=0)
    hashtags = models.TextField()
    
    def __str__(self) -> str:
        return f'{self.post_id} -> {self.user}'
            
class Postlikes(models.Model):
    like_id = models.UUIDField(default=uuid.uuid1, editable=False, unique=True)
    post_id = models.ForeignKey(Post,on_delete=models.CASCADE)
    user_id = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return self.post_id.post_id
    
class Postcomment(models.Model):
    comment_id = models.UUIDField(default=uuid.uuid1, editable=False, unique=True)
    post_id = models.ForeignKey(Post,on_delete=models.CASCADE)
    user_id = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return self.post_id.post_id
    
class Follows(models.Model):
    follower = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="follower")
    following = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return self.follower.username
    
class stories(models.Model):
    story_id = models.UUIDField(default=uuid.uuid4,editable=False,unique=True,primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    story_url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.story_id}'