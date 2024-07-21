from django.db import models

from api.models.tools_model import Tools
from api_auth.User.UserModel import User
from payment.models.rental_order_model import RentalOrder


class ToolsHistory(models.Model):
    tools_history_id = models.AutoField(primary_key=True)
    tool = models.ForeignKey(Tools, on_delete=models.CASCADE)
    rental_order = models.ForeignKey(RentalOrder, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    rent_start_date = models.DateTimeField()
    rent_end_date = models.DateTimeField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
