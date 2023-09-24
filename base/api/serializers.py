from rest_framework import serializers
from base.models import Profile
from django.contrib.auth import get_user_model

User = get_user_model()


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')

    def create(self, validated_data):
        username = validated_data['username']
        password = validated_data['password']

        # Check if the username already exists
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError({'username': 'This username is already in use.'})
        
        user = User(username=username)
        user.set_password(password)
        user.save()
        return user
    

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'username', 'bio', 'profile_image']    


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['username']  


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('id', 'username', 'bio', 'profile_image')   


class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('username', 'bio', 'profile_image')


