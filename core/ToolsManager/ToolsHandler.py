from django.db.models import F, Count, Q
from rest_framework import status
from rest_framework.response import Response

from api.Models.tools_category_model import ToolsCategory
from api.Models.tools_model_model import ToolsModel
from api.Serializers.serializers import (ToolsSerializer, ToolsModelSerializer, ToolsHistorySerializer)
from core.ToolsManager.ToolsHelper import ToolsHelper


class ToolsHandler:

    @staticmethod
    def handler_get_all_tools():
        try:
            # Get all tools.
            tools_objects = ToolsHelper.get_all_tools_objects()
            if tools_objects:
                # If tools were found, serialize it and return the data.
                tools_ser = ToolsSerializer(tools_objects, many=True)
                return Response(tools_ser.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'user_error': "Something went wrong, please try again later or contact support.",
                             "dev_error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'user_error': "No tools were found."}, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def handler_get_all_tools_models():
        try:
            # Get the tools models
            tools_models_objects = ToolsHelper.get_all_tools_models_objects()

            # for each model, adds a counter with the amount of available tools of that model.
            tools_models_objects = tools_models_objects.annotate(
                amount_available=Count(F("tools__id"), filter=Q(tools__available=True)))
            if tools_models_objects:
                # If tools where found, serialize and return the data.
                tools_models_ser = ToolsModelSerializer(tools_models_objects, many=True)
                return Response(tools_models_ser.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'user_error': "Something went wrong, please try again later or contact support.",
                             "dev_error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'user_error': "No tools were found."}, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def handler_get_tool(tool_id):
        try:
            tool = ToolsHelper.get_tool_by_id(tool_id)
            tool_serialized = ToolsSerializer(tool)
            return Response(tool_serialized.data, status=status.HTTP_200_OK)

        except ToolsModel.DoesNotExist:
            return Response(f"No tool was found with ID {tool_id}", status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'user_error': "Something went wrong, please try again later or contact support.",
                             "dev_error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def handler_get_tools_by_category(request):
        try:
            category_name = request.GET.get('category_name')

            if not category_name:
                return Response({'error': 'category parameter is required'}, status=status.HTTP_400_BAD_REQUEST)

            category = ToolsCategory.objects.get(name=category_name)

            tools = ToolsHelper.get_tools_by_category(category)

            if not tools.exists():
                return Response(f"No tools found for this category: {category_name}", status=status.HTTP_404_NOT_FOUND)

            tools_serialized = ToolsSerializer(tools, many=True)
            return Response(tools_serialized.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'user_error': "Something went wrong, please try again later or contact support.",
                             "dev_error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @staticmethod
    def handler_get_tools_history_by_user(user):
        try:
            history_objects = ToolsHelper.get_tools_history_by_user(user)
            if history_objects:
                history_objects = ToolsHelper.get_related_tools_history(history_objects)
                history_serializer = ToolsHistorySerializer(history_objects, many=True)
                return Response(history_serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({'user_error': "No tool rental were found for this user.",
                                 "dev_error": "No tool rental were found for this user."},
                                status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'user_error': "Something went wrong, please try again later or contact support.",
                             "dev_error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
