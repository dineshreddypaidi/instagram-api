from rest_framework import serializers
from users import models as usermodels

class loggeduserserialzer(serializers.ModelSerializer):
    class Meta:
        model = usermodels.CustomUser
        exclude = ["is_superuser","password","is_staff","groups","user_permissions"]
        read_only_fields = ("__all__",)
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = usermodels.CustomUser
        fields = '__all__'
        
    def create(self, validated_data):
        user = usermodels.CustomUser(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            instance.set_password(validated_data['password'])
            validated_data.pop('password')
        
        return super().update(instance, validated_data)
                
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
        lookup_filed = 'post_id'
        
class userfollowsserailizer(serializers.ModelSerializer):  
    class Meta:
        model = usermodels.Follows
        fields = '__all__'                 
        
class storiesserailizer(serializers.ModelSerializer):  
    class Meta:
        model = usermodels.stories
        fields = '__all__'      
        
        
#users view for everyone      
class UserviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = usermodels.CustomUser
        exclude = ['password',]
        lookup_field = "username"
class UserPostviewserailizer(serializers.ModelSerializer):  
    class Meta:
        model = usermodels.Post
        fields = '__all__'
        read_only_fields = ("__all__",)
        lookup_field = "username"