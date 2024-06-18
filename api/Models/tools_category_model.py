from django.db import models


class ToolsCategory(models.Model):
    name = models.CharField(max_length=100)
