from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from api_auth.User.UserModel import User
from api_auth.User.serializers import (UserSerializer, UserUpdateSerializer, UserInfoSerializer)
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

    @staticmethod
    def handler_user_registration(request_data):

        """
        """
        try:

            request_data['username'] = request_data.get('email')
            user_serializer = UserSerializer(data=request_data)
            if user_serializer.is_valid():
                user_serializer.save()
            else:
                return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except ValueError as e:
            return Response("Error occuned during registration flow.", status=status.HTTP_400_BAD_REQUEST)
        return Response("User registration was successful.", status=status.HTTP_201_CREATED)


    @staticmethod
    def handler_user_update(request_data, user):
        """
        Handler for updating user information. It validates the passed values and updated only the passed fields.
        Updatable fields:
        - first_name
        - last_name
        - address
        - phone_number

        :param request_data:
        :param user:
        :return:
        """

        user_serializer = UserUpdateSerializer(user, data=request_data)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response(user_serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def handler_get_user_info(user):
        """
        Handler for getting user info.

        :param user_id:
        :return: dict with user info - first name, last name, email,address, phone number
        """
        try:
            serialized_user = UserInfoSerializer(user)

            if serialized_user:
                return Response(serialized_user.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'user_error': "Something went wrong, please try again later or contact support.",
                                "dev_error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            
        return Response({'user_error': "No user was found."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    @staticmethod
    def handler_user_change_password(request_data, user):
        """
        Handler for changing user password

        :param user:
        :param request_data:
        :return: success message
        """

        if not "password" in request_data or request_data.get('password') is None:
            return Response("Password must be passed in and cannot be null or empty", status = status.HTTP_400_BAD_REQUEST)

        UserHelper.validate_password(request_data.get('password'))

        if user:
            user.set_password(request_data.get('password'))

            return Response("Password has been updated successfully.", status=status.HTTP_200_OK)
        else:
            return Response(validated_data.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
