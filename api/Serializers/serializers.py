from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from api.Models.tools_category_model import ToolsCategory
from api.Models.tools_history_model import ToolsHistory
from api.Models.tools_model import Tools
from api.Models.tools_model_model import ToolsModel


class ToolsSerializer(ModelSerializer):
    class Meta:
        model = Tools
        fields = '__all__'
        depth = 2


class ToolsModelSerializer(ModelSerializer):
    amount_available = serializers.IntegerField(min_value=0, default=0, read_only=True)

    class Meta:
        model = ToolsModel
        fields = '__all__'
        depth = 1


class ToolsHistorySerializer(ModelSerializer):
    class Meta:
        model = ToolsHistory
        exclude = ('user',)
        depth = 3


class ToolsCategorySerializer(ModelSerializer):
    class Meta:
        model = ToolsCategory
        fields = '__all__'
