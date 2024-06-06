from rest_framework import serializers

from api_auth.User.UserModel import User


# TODO: Remove this temporary serializer
class UserSerializer(serializers.ModelSerializer):
    """
    Temporary serializer for initial testings. Must be removed as soon as frontend is ready to call APIs
    """

    class Meta:
        model = User
        fields = '__all__'
