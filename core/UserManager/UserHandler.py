from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from api_auth.User.UserModel import User
from api_auth.User.serializers import UserSerializer


class UserHandler:
    @staticmethod
    def handler_user_login(request_data):
        """
        References: https://django-rest-framework-simplejwt.readthedocs.io/en/latest/creating_tokens_manually.html
        https://docs.djangoproject.com/en/5.0/topics/auth/customizing/#authentication-backends
        :param request_data:
        :return:
        """
        email = request_data.get('username')
        password = request_data.get('password')
        if email and password:
            try:
                print(email)
                print(password)
                user = User.objects.get(email__exact=email)
            except User.DoesNotExist:
                return Response('User does not exist', status=status.HTTP_400_BAD_REQUEST)

            if user.check_password(password):
                # The user exists and the password is correct then create a Token and return it.
                token = RefreshToken.for_user(user)
                response_data = {'refresh': str(token),
                                 'access': str(token.access_token)}
                return Response(data=response_data, status=status.HTTP_200_OK)

        return Response('Invalid credentials', status=status.HTTP_400_BAD_REQUEST)

    # TODO: Remove this temporary handler
    @staticmethod
    def handler_users_list(request):
        """
            Temporary handler for initial testings. Must be removed as soon as frontend is ready to call APIs
        """
        user_list = User.objects.all().values()
        print(user_list)
        ser = UserSerializer(user_list, many=True)
        return Response(data=ser.data, status=status.HTTP_200_OK)
