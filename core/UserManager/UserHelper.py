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
    def serialize_user_info(user):
        return {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "address": user.address,
            "phone_number": user.phone_number
        }