from rest_framework import serializers
from users import models as usermodels

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

