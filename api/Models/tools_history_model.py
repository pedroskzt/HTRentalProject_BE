from django.db import models

from api.Models.tools_model import Tools
from api_auth.User.UserModel import User


class ToolsHistory(models.Model):
    tool = models.ForeignKey(Tools, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    rent_start_date = models.DateField()
    rent_end_date = models.DateField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
