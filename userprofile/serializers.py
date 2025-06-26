from django.contrib.auth import get_user_model
from rest_framework import serializers

from userprofile.models import UserProfile

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'
        read_only_fields = ['user']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation.pop('user')
        user_representation = UserSerializer(instance.user).data
        for key in user_representation:
            representation[key] = user_representation[key]
        return representation
