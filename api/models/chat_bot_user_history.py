from django.db import models

from api_auth.User.UserModel import User


class ChatBotUserHistory(models.Model):
    bot_history_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chat_history = models.BinaryField(null=True, editable=True)
    active = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
