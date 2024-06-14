from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from api_auth.User.UserModel import User
from core.UserManager.UserHelper import UserHelper


class UserHandler:
    @staticmethod
    def handler_user_login(request_data):
        """
        Handler for login in the user.
        References: https://django-rest-framework-simplejwt.readthedocs.io/en/latest/creating_tokens_manually.html
        https://docs.djangoproject.com/en/5.0/topics/auth/customizing/#authentication-backends
        :param request_data: Username and password in JSON format.
        :return: JSON response with HTTP status code.
        """
        email = request_data.get('username')
        password = request_data.get('password')
        if email and password:
            try:
                user = UserHelper.get_user_by_email(email)
            except User.DoesNotExist:
                return Response('User does not exist', status=status.HTTP_400_BAD_REQUEST)

            if user.check_password(password):
                # The user exists and the password is correct then create a Token and return it.
                token = RefreshToken.for_user(user)
                response_data = {'refresh': str(token),
                                 'access': str(token.access_token)}
                return Response(data=response_data, status=status.HTTP_200_OK)

        return Response('Invalid credentials', status=status.HTTP_400_BAD_REQUEST)
