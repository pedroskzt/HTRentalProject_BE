from rest_framework import status
from rest_framework.response import Response

from core.CustomErrors.CustomErrors import CustomError


class ChatBotHandler:

    @staticmethod
    def handler_get_chat_bot_response():
        try:
            # TODO: processing of input and calling google gemini api
            return Response("stub", status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'user_error': "Something went wrong, please try again later or contact support.",
                             "dev_error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"stub"}, status=status.HTTP_400_BAD_REQUEST)