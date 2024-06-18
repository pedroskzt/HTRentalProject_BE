from django.db import models

from api.Models.tools_model_model import ToolsModel


class Tools(models.Model):
    model = models.ForeignKey(ToolsModel, on_delete=models.SET_NULL, null=True)
    available = models.BooleanField(default=False)

    def __str__(self):
        return str(self.model)