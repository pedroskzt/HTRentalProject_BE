from django.db import models

from api.Models.tools_category_model import ToolsCategory
from api.Models.tools_model_model import ToolsModel


class Tools(models.Model):
    category = models.ForeignKey(ToolsCategory, on_delete=models.SET_NULL, null=True)
    model = models.ForeignKey(ToolsModel, on_delete=models.SET_NULL, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(null=True)
    available = models.BooleanField(default=True)
    image_name = models.TextField(null=True)
