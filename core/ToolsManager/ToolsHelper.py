from django.db.models import F, Count, Q

from api.Models.tools_category_model import ToolsCategory
from api.Models.tools_history_model import ToolsHistory
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
        :return: ToolsModel queryset
        """
        return ToolsModel.objects.all()

    @staticmethod
    def get_model_by_id(model_id):
        """
        Get a tools model by id.
        :param model_id:
        :return: ToolsModel queryset
        """
        return ToolsModel.objects.filter(id=model_id)

    @staticmethod
    def get_tool_by_id(id):
        """
        Get all tools models objects.
        :return:
        """
        return Tools.objects.get(id=id)

    @staticmethod
    def get_tool_category_by_name(category_name):
        return ToolsCategory.objects.filter(name=category_name)

    @staticmethod
    def get_tools_models_by_category(category):
        """
        Get all tools models objects of the corresponding category.
        :return:
        """
        return ToolsModel.objects.filter(category=category)

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
        :param ToolsHistory queryset:
        :return:
        """
        return queryset.select_related('tool', 'tool__model', 'tool__model__category')

    @staticmethod
    def get_related_tools_models(queryset):
        """
        Get category information related to each model/branch on the queryset.
        This method is mainly to optimize the serialization process.
        :param ToolsModel queryset:
        :return:
        """
        return queryset.select_related('category')

    @staticmethod
    def count_available_tools_by_model(queryset):
        """
        Add am amount_available field on the queryset with the count of available tools for each model on the queryset.
        :param ToolsModel queryset:
        :return:
        """
        return queryset.annotate(amount_available=Count(F("tools__id"), filter=Q(tools__available=True)))

    @staticmethod
    def check_tool_exists(model, brand):
        """
        Returns true if tool with given model, brand exists, otherwise false.
        :param model:
        :param brand:
        :return: boolean
        """
        return ToolsModel.objects.filter(model=model, brand=brand)