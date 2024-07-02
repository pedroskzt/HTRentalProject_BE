from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

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


class GetToolsModelById(APIView):
    """
    View responsible for returning the model corresponding to the given id.
    """

    def get(self, request, model_id):
        return ToolsHandler.handler_get_tools_model_by_id(model_id)


class GetTool(APIView):
    """
    View responsible for returning a tool given an ID.
    """

    def get(self, request, tool_id):
        return ToolsHandler.handler_get_tool(tool_id)


class GetToolsByCategory(APIView):
    """
    View responsible for returning a list of tools given a category.
    """

    def get(self, request, category_id):
        return ToolsHandler.handler_get_tools_by_category(category_id)


class GetToolsHistoryByUser(APIView):
    """
    View responsible for returning a list of tools and its information for each tool rented by the user.
    Requires the user to be logged in.
    """

    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)

    def get(self, request):
        return ToolsHandler.handler_get_tools_history_by_user(request.user)

class GetAllCategories(APIView):
    """
        View responsible for returning a list of all categories.
        """

    def get(self, request):
        return ToolsHandler.handler_get_all_categories()