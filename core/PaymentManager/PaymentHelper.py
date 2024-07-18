from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response

from core.CustomErrors.CustomErrors import CustomError
from payment.models.rental_cart_model import RentalCart
from payment.models.rental_cart_model import RentalCartItem
from payment.models.rental_order_model import RentalOrder
from payment.models.rental_order_model import RentalOrderItem


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

    @staticmethod
    def get_rental_orders_by_user(user):
        return RentalOrder.objects.filter(user=user)

    @staticmethod
    def get_all_rental_order_items(rental_order):
        return RentalOrderItem.objects.filter(rental_order=rental_order)

    @staticmethod
    def validate_rental_order(rental_order):
        """
        Validate the rental order queryset for the most recent rental order and check if it has not expired.
        :param rental_order: RentalOrder queryset
        :return: RentalOrder object if most recent order is still valid, False otherwise
        """
        if rental_order.exists():
            rental_order = rental_order.latest('date_created')
            # Check if the most recent order is older than 1 day and Status is Opened. If so Cancel it.
            if rental_order.status == rental_order.OPEN and (timezone.now() - rental_order.date_created).days > 0:
                # This order is too old, cancel it and make the items on it available.
                rental_order.tools.through.objects.all().update(available=True)
                rental_order.status = rental_order.CANCELLED
                rental_order.save()
            else:
                return rental_order
        return False

    @staticmethod
    def validate_rental_cart(user):
        # Check if user has items on the rental cart.
        rental_cart = PaymentHelper.get_rental_cart_by_user(user)
        if rental_cart.exists() is False:
            return False, Response(CustomError.get_error_by_code("PRC-2", rental_cart.errors),
                                   status=status.HTTP_400_BAD_REQUEST)
        rental_cart = rental_cart.first()

        # Check if the existing rental cart has expired
        if (timezone.now() - rental_cart.date_updated).days > 0:
            rental_cart.delete()
            return False, Response(CustomError.get_error_by_code("PRC-2", "Rental Cart Expired."),
                                   status=status.HTTP_400_BAD_REQUEST)

        return rental_cart, Response(status=status.HTTP_200_OK)
