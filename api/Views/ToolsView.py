from rest_framework.views import APIView

from core.ToolsManager.ToolsHandler import ToolsHandler


class GetAllTools(APIView):
    """
    View responsible for returning all tools and its information.
    """

    def get(self, request):
        return ToolsHandler.handler_get_all_tools()


class GetAllToolsModels(APIView):
    """
    View responsible for returning all tools model, its information and amount available of each model.
    """

    def get(self, request):
        return ToolsHandler.handler_get_all_tools_models()
