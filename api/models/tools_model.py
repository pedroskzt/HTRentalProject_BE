from django.db import models

from api.models.tools_model_model import ToolsModel


class Tools(models.Model):
    tool_id = models.AutoField(primary_key=True)
    model = models.ForeignKey(ToolsModel, on_delete=models.SET_NULL, null=True)
    available = models.BooleanField(default=False)

    def __str__(self):
        return str(self.model)
