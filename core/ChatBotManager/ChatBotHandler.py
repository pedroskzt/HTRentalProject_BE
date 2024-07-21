from rest_framework import status
from rest_framework.response import Response
from django.utils import timezone
from core.ChatBotManager.ChatBotHelper import ChatBotHelper
from core.CustomErrors.CustomErrors import CustomError
from types import SimpleNamespace


class ChatBotHandler:

    @staticmethod
    def handler_get_chat_bot_response(request_data, user):
        try:
            user_history_obj = None
            if user.is_authenticated:
                user_history_obj = ChatBotHelper.get_user_history(user)
                if user_history_obj.exists() and (timezone.now() - user_history_obj.latest('date_created').date_created).days <= 0:
                    user_history_obj = user_history_obj.latest('date_created')
                else:
                    if user_history_obj.exists():
                        user_history_obj = user_history_obj.latest('date_created')
                        user_history_obj.active = False
                        user_history_obj.save()

                    user_history_obj = ChatBotHelper.create_user_history(user)

            user_chat = ChatBotHelper.initiate_chat(user_history_obj, user)

            # bot_msg = ChatBotHelper.send_gemini_request(model, request_data.get("input"))
            user_msg = request_data.get("input")
            if user_msg:
                responses = user_chat.send_message(user_msg, stream=True)
            else:
                return Response(CustomError.error_dictionary("CB-0"), status=status.HTTP_400_BAD_REQUEST)

            bot_msg = ""
            for response in responses:
                text = response.text
                bot_msg += text

            if user.is_authenticated:
                ChatBotHelper.update_user_history(user_history_obj, user_chat)

            return Response(ChatBotHelper.process_response(bot_msg), status=status.HTTP_200_OK)
        except Exception as e:
            return Response(CustomError.get_error_by_code("GE-0", e), status=status.HTTP_400_BAD_REQUEST)
