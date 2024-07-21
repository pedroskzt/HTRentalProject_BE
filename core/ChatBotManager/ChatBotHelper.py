import json
import pickle
import re

import vertexai
from django.conf import settings
from vertexai.generative_models import GenerativeModel

from api.models.chat_bot_user_history import ChatBotUserHistory
from core.ToolsManager.ToolsHelper import ToolsHelper


class ChatBotHelper:

    @staticmethod
    def get_user_history(user):
        """
        Get chat-bot history for a given user.
        :param user:
        :return:
        """
        return ChatBotUserHistory.objects.filter(user=user)

    @staticmethod
    def create_user_history(user):
        """
        Create chat-bot history for a given user.
        :param user:
        :return:
        """
        chat_history_obj = ChatBotUserHistory(user=user)
        chat_history_obj.save()
        return chat_history_obj

    @staticmethod
    def initiate_chat(user_history_obj, user):
        """
        Initialization of the chat-bot model. Defines the system instructions to the model and create chat object.
        :param user_history_obj: ChatBotUserHistory object
        :param user: api_auth User
        :return: Gemini Chat Object
        """
        vertexai.init(project=settings.PROJECT_ID, location=settings.REGION)

        tools_model_list = list(ToolsHelper.get_all_tools_models_objects().values("brand", "model", "description"))
        system_instructions = ["You are the support chat bot of a tool rental company called Handy Tools Rental.",
                               "You are going to help a customer to choose the best tool for his needs.",
                               "You should always informe the brand and model of the tool",
                               "If you make a suggestion, you must include at the end of your message JSON list with the suggested tools and with the following identifier: JSON->."
                               f"Here is a JSON list with all tools that we have.\n{tools_model_list}",
                               f"This customer is called {user.get_full_name()}"]
        model = GenerativeModel(model_name=settings.MODEL_NAME, system_instruction=system_instructions)

        user_history = user_history_obj.chat_history
        user_history = pickle.loads(user_history) if user_history else user_history
        return model.start_chat(history=user_history)

    @staticmethod
    def update_user_history(user_history_obj, user_chat):
        """
        Updates the Chat-bot chat history for a given user.
        :param user_history_obj: ChatBotUserHistory object
        :param user_chat: Gemini Chat object
        :return:
        """
        user_history_obj.chat_history = pickle.dumps(user_chat.history)
        user_history_obj.save()
        return user_history_obj

    @staticmethod
    def process_response(response):
        """
        Filters the response string for a JSON at the end with the suggested tools.
        :param response: Response string from Gemini.
        :return: {
        response_to_user -> Gemini Response without the JSON
        suggested_tools -> Suggested tools parsed to Python Json Object
        }
        """
        response_to_user = response
        suggested_tools = None

        startJson = response.find("JSON->")
        if startJson > -1:
            endJson = re.search("](\s)*\n", response)
            if endJson is not None:
                endJson = endJson.start() + 1

                response_to_user = response[:startJson] + response[endJson:]
                dirt_json = response[startJson:endJson]

                startJson = dirt_json.find("[")
                endJson = dirt_json.find("]") + 1
                dirt_json = dirt_json[startJson:endJson]
                suggested_tools = json.loads(dirt_json.replace("'", '"'))

        return {"response_to_user": response_to_user,
                "suggested_tools": suggested_tools}
