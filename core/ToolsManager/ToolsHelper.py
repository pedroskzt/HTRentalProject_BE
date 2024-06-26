from api.Models.tools_category_model import ToolsCategory
from api.Models.tools_model import Tools
from api.Models.tools_model import ToolsModel
from api.Models.tools_history_model import ToolsHistory


class ToolsHelper:

    @staticmethod
    def get_all_tools_objects():
        """
        Get all tools objects.
        :return:
        """
        return Tools.objects.all()

    @staticmethod
    def get_all_tools_models_objects():
        """
        Get all tools models objects.
        :return:
        """
        return ToolsModel.objects.all()
    
    @staticmethod
    def get_tool_by_id(id):
        """
        Get all tools models objects.
        :return:
        """
        return Tools.objects.get(id=id)
        
    @staticmethod
    def get_tools_by_category(category):
        """
        Get all tools models objects.
        :return:
        """
        return Tools.objects.filter(model__category=category)

    @staticmethod
    def get_tools_history_by_user(user):
        """
        Get all tools history by user.
        :param user:
        :return:
        """
        return ToolsHistory.objects.filter(user=user)

    @staticmethod
    def get_related_tools_history(queryset):
        """
        Get model and category information related to each tool on the queryset.
        This method is mainly to optimize the serialization process.
        :param queryset:
        :return:
        """
        return queryset.select_related('tool', 'tool__model', 'tool__model__category')
