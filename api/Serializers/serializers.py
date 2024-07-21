from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, SlugRelatedField, SerializerMethodField

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
    rental_order = SlugRelatedField(read_only=True, slug_field='pk')
    rental_price = SerializerMethodField(read_only=True)
    user = SlugRelatedField(read_only=True, slug_field='pk')

    class Meta:
        model = ToolsHistory
        fields = '__all__'
        depth = 3

    def get_rental_price(self, obj):
        days = (obj.rent_end_date - obj.rent_start_date).days
        return days * obj.tool.model.price


class LightToolsHistorySerializer(ModelSerializer):
    class Meta:
        model = ToolsHistory
        fields = '__all__'


class ToolsCategorySerializer(ModelSerializer):
    class Meta:
        model = ToolsCategory
        fields = '__all__'
