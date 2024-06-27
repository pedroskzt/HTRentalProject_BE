from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from core.UserManager.UserHandler import UserHandler


class UserLogin(APIView):
    """
    View responsible for loging in the user
    """

    def post(self, request):
        return UserHandler.handler_user_login(request_data=request.data)


class UserRegistration(APIView):
    """
    View responsible for registering the user
    """

    def post(self, request):
        return UserHandler.handler_user_registration(request_data=request.data)


class UserUpdate(APIView):
    """
    View responsible for returning a list of tools and its information for each tool rented by the user.
    """

    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)

    def post(self, request):
        try:
            return UserHandler.handler_user_update(request.data, request.user)
        except Exception as e:
            return Response({'user_error': "Something went wrong, please try again later or contact support.",
                             "dev_error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
