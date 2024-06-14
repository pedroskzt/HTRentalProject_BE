from rest_framework import serializers

from api_auth.User.UserModel import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
