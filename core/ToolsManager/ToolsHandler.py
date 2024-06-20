from django.db.models import F, Count, Q
from rest_framework import status
from rest_framework.response import Response

from api.Serializers.serializers import (ToolsSerializer, ToolsModelSerializer)
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
