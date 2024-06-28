from rest_framework import serializers

from api_auth.User.UserModel import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # Create a user object with all validated fields.
        user_obj = User(**validated_data)

        # Encrypt and set the password to this user.
        user_obj.set_password(validated_data['password'])

        # Save the user in the database
        user_obj.save()
        return user_obj


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'address', 'phone_number')

    def validate_first_name(self, value):
        if len(value) <= 0:
            raise serializers.ValidationError('First name cannot be empty')

        return value

    def validate_last_name(self, value):
        if len(value) <= 0:
            raise serializers.ValidationError('Last name cannot be empty')

        return value

    def validate_address(self, value):
        if len(value) <= 0:
            raise serializers.ValidationError('Address cannot be empty')

        return value

    def validate_phone_number(self, value):
        if len(value) <= 0:
            raise serializers.ValidationError('Phone number cannot be empty')

        return value
