from api.Models.tools_category_model import ToolsCategory
from api.Models.tools_model import Tools
from api.Models.tools_model import ToolsModel


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
