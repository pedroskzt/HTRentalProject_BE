from django.contrib.auth.models import Group

from api_auth.User.UserModel import User


class UserHelper:
    @staticmethod
    def get_user_by_email(email):
        # Get a user object by exact email and return it.
        return User.objects.get(email__exact=email)

    @staticmethod
    def get_manager_group():
        return Group.objects.filter(name='Manager')
