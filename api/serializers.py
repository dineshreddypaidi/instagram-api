from rest_framework import serializers
from users import models as usermodels

class User_registerSerializer(serializers.ModelSerializer):
    class Meta:
        model = usermodels.CustomUser
        fields = ["username","email","bio","name","profile_image_url","website_url","account_type","password"]
        extra_kwargs = {'password': {'write_only': True}}
        
    def create(self, validated_data):
        password = validated_data.pop('password') 
        user = usermodels.CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            instance.set_password(validated_data['password'])
        
        return super().update(instance, validated_data) 
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = usermodels.CustomUser
        exclude = ["is_superuser","password","is_staff","groups","user_permissions"]
        lookup_field = "username"
                    
class Postserailizer(serializers.ModelSerializer):  
    class Meta:
        model = usermodels.Post
        #fields = '__all__'
        exclude = ['user',]
        
    def create(self, validated_data):
        return super().create(validated_data)
class Postlikeserailizer(serializers.ModelSerializer):  
    class Meta:
        model = usermodels.Postlikes
        fields = '__all__'
        lookup_filed = 'post_id'
                
class Postcommentserailizer(serializers.ModelSerializer):  
    class Meta:
        model = usermodels.Postcomment
        fields = '__all__'
        lookup_field = 'post_id'
        
class userfollowserailizer(serializers.ModelSerializer):  
    class Meta:
        model = usermodels.Follows
        fields = '__all__'             
        
class userstoriesserailizer(serializers.ModelSerializer):  
    class Meta:
        model = usermodels.stories
        fields = '__all__'      
              
#users view for everyone
class UserPostviewserailizer(serializers.ModelSerializer):
    class Meta:
        model = usermodels.Post
        fields = '__all__'
        read_only_fields = ("__all__",)
        lookup_field = "username"