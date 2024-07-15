from django.conf import settings
from django.db import models

from api.Models.tools_model_model import ToolsModel


class RentalCart(models.Model):
    tools = models.ManyToManyField(ToolsModel, through='RentalCartItem')
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)


class RentalCartItem(models.Model):
    rental_cart = models.ForeignKey(RentalCart, on_delete=models.CASCADE)
    tool = models.ForeignKey(ToolsModel, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    rental_time = models.IntegerField()
