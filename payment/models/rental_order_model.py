from django.conf import settings
from django.db import models

from api.models.tools_model import Tools


class RentalOrder(models.Model):
    # Status Choices
    COMPLETED = "completed"
    OPEN = "open"
    CANCELLED = "cancelled"

    status_choices = [
        (COMPLETED, "Completed"),
        (OPEN, "Open"),
        (CANCELLED, "Cancelled"),
    ]

    rental_order_id = models.AutoField(primary_key=True)
    tools = models.ManyToManyField(Tools, through='RentalOrderItem')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    status = models.CharField(choices=status_choices, default=OPEN, max_length=50)
    sub_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    date_completed = models.DateTimeField(null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)


class RentalOrderItem(models.Model):
    rental_order_item_id = models.AutoField(primary_key=True)
    rental_order = models.ForeignKey(RentalOrder, on_delete=models.CASCADE)
    tool = models.ForeignKey(Tools, on_delete=models.CASCADE)
    time_rented = models.IntegerField()
