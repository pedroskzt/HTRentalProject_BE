from rest_framework.views import APIView

from core.UserManager.UserHandler import UserHandler


class UserLogin(APIView):
    """
    View responsible for loging in the user
    """

    def post(self, request):
        return UserHandler.handler_user_login(request_data=request.data)
