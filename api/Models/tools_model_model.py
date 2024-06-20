from django.db import models


class ToolsModel(models.Model):
    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
