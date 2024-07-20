from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from api.models.tools_category_model import ToolsCategory
from api.models.tools_history_model import ToolsHistory
from api.models.tools_model import Tools
from api.models.tools_model_model import ToolsModel


class ToolsSerializer(ModelSerializer):
    class Meta:
        model = Tools
        fields = '__all__'
        depth = 3

    def create(self, validated_data):
        validated_data['model'] = self.context.get('model')
        tool = Tools(**validated_data)
        tool.save()
        return tool

    def update(self, instance, validated_data):
        instance.available = validated_data.get('available', instance.available)
        instance.model = self.context.get('model', instance.model)
        instance.save()
        return instance


class ToolsModelSerializer(ModelSerializer):
    amount_available = serializers.IntegerField(min_value=0, default=0, read_only=True)

    class Meta:
        model = ToolsModel
        fields = '__all__'
        depth = 1

    def create(self, validated_data):
        validated_data['category'] = self.context.get('category')
        tools_model = ToolsModel(**validated_data)
        tools_model.save()
        return tools_model


class ToolsHistorySerializer(ModelSerializer):
    class Meta:
        model = ToolsHistory
        exclude = ('user',)
        depth = 3


class LightToolsHistorySerializer(ModelSerializer):
    class Meta:
        model = ToolsHistory
        fields = '__all__'
    # def create(self, validated_data):
    #     validated_data['user'] = self.context['user']
    #     validated_data['tool'] = self.context['tool']
    #     tools_history = ToolsHistory(**validated_data)
    #     tools_history.save()
    #     return tools_history


class ToolsCategorySerializer(ModelSerializer):
    class Meta:
        model = ToolsCategory
        fields = '__all__'
