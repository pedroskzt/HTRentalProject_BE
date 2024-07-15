from django.utils import timezone

from payment.models.rental_cart_model import RentalCart
from payment.models.rental_cart_model import RentalCartItem


class PaymentHelper:

    @staticmethod
    def get_rental_cart_by_user(user):
        return RentalCart.objects.filter(user=user)

    @staticmethod
    def update_rental_cart_last_modified(rental_cart_obj):
        rental_cart_obj.date_updated = timezone.now()
        rental_cart_obj.save()

    @staticmethod
    def get_all_rental_cart_items(rental_cart):
        return RentalCartItem.objects.filter(rental_cart=rental_cart)
