from rest_framework import status
from rest_framework.response import Response

from core.CustomErrors.CustomErrors import CustomError


class ChatBotHandler:

    @staticmethod
    def handler_get_chat_bot_response(request):
        try:
            # TODO: processing of input and calling google gemini api
            return Response("stub", status=status.HTTP_200_OK)
            # return Response({"stub"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(CustomError.get_error_by_code("GE-0", e), status=status.HTTP_400_BAD_REQUEST)

