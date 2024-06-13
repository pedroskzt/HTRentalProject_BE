from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from core.UserManager.UserHandler import UserHandler


class UserLogin(APIView):
    """
    View responsible for loging in the user
    """

    def post(self, request):
        return UserHandler.handler_user_login(request_data=request.data)

# TODO: Remove this temporary view
class UsersList(APIView):
    """
        Temporary handler for initial testings. Must be removed as soon as frontend is ready to call APIs
    """
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        return UserHandler.handler_users_list(request)

class UserRegistration(APIView):
    """
    View responsible for registering the user
    """

    def post(self, request):
        return UserHandler.handler_user_registration(request_data=request.data)
