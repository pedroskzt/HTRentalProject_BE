from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from core.ChatBotManager.ChatBotHandler import ChatBotHandler
from core.ToolsManager.ToolsHandler import ToolsHandler


class GetChatBotResponse(APIView):
    """
    View responsible for processing input and returning chat bot response.
    """
    permission_classes = (AllowAny,)
    # authentication_classes = (JWTAuthentication,)

    def post(self, request):
        return ChatBotHandler.handler_get_chat_bot_response(request.data, request.user)
        # return ToolsHandler.handler_get_all_tools_models()
