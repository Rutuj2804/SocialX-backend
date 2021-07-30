from .models import UserProfile
from rest_framework import serializers


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'
        depth = 2


class DisplayPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['photo']
