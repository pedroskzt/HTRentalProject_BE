from django.db import models

from api.models.tools_category_model import ToolsCategory


class ToolsModel(models.Model):
    class Meta:
        unique_together = [["brand", "model"]]

    tools_model_id = models.AutoField(primary_key=True)
    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    name = models.CharField(max_length=50, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    category = models.ForeignKey(ToolsCategory, on_delete=models.SET_NULL, null=True)
    description = models.TextField(null=True)
    image_name = models.TextField()

    def __str__(self):
        return str(self.description)
