from rest_framework.serializers import ModelSerializer

from api.Models.tools_model import Tools


class ToolsSerializer(ModelSerializer):
    class Meta:
        model = Tools
        fields = '__all__'
        depth = 1