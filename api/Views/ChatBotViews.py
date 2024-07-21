from rest_framework.views import APIView

from core.ChatBotManager.ChatBotHandler import ChatBotHandler


class GetChatBotResponse(APIView):
    """
    View responsible for processing input and returning chat bot response.
    """

    def get(self, request):
        return ChatBotHandler.handler_get_chat_bot_response(request.data, request.user)
