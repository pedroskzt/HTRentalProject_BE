from api_auth.User.UserModel import User


class UserHelper:
    @staticmethod
    def get_user_by_email(email):
        # Get a user object by exact email and return it.
        return User.objects.get(email__exact=email)

    @staticmethod
    def get_user_by_id(id):
        return User.objects.get(id=id)

    @staticmethod
    def validate_password(password):
        if len(password) <= 10:
            raise serializers.ValidationError('Password must be greater than 10 characters')
        elif not any(character.isdigit() for character in password):
            raise serializers.ValidationError('Password must contain at least 1 number')

        return password