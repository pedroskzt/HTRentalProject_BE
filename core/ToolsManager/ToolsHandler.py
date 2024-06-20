from rest_framework import status
from rest_framework.response import Response

from api.Serializers.serializers import ToolsSerializer
from core.ToolsManager.ToolsHelper import ToolsHelper


class ToolsHandler:

    @staticmethod
    def handler_get_all_tools():
        try:
            tools_objects = ToolsHelper.get_all_tools_objects()
            if tools_objects:
                tools_ser = ToolsSerializer(tools_objects, many=True)
                return Response(tools_ser.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'user_error': "Something went wrong, please try again later or contact support.",
                             "dev_error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'user_error': "No tools were found."}, status=status.HTTP_400_BAD_REQUEST)
