from rest_framework import serializers
from .models import Group


class GroupSerailizer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'
        depth = 2