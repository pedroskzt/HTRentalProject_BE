from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response

from core.CustomErrors.CustomErrors import CustomError
from core.PaymentManager.PaymentHelper import PaymentHelper
from core.ToolsManager.ToolsHelper import ToolsHelper
from payment.Serializers.serializers import (RentalCartSerializer, RentalCartItemSerializer)


class PaymentHandler:
    @staticmethod
    def handler_add_tool_model_to_cart(request_data, user):
        """
        Adds the selected tool model to the rental cart.
        :param request_data: {
        "tools_model_id": <integer>,
        "rental_time": <integer>,
        "quantity": <integer>
        }
        :param user: User object.
        :return:
        """
        try:
            tools_model = ToolsHelper.get_model_by_id(request_data.get('tools_model_id'))
            if tools_model.exists() is False:  # Check if the informed Tool Model exists.
                return Response(CustomError.get_error_by_code("TM-0"), status=status.HTTP_400_BAD_REQUEST)
            tools_model = tools_model.first()  # Get the tool model object

            rental_cart = PaymentHelper.get_rental_cart_by_user(user)
            if rental_cart.exists() is False or (timezone.now() - rental_cart.first().date_updated).days > 0:
                # Check if a cart for this user already exists. If not, create one.
                # Also checks if the last update on the cart was 24 hours+. If so, delete and create new one.
                if rental_cart.first():
                    rental_cart.first().delete()
                rental_cart_ser = RentalCartSerializer(data={'user': user.pk})
                if rental_cart_ser.is_valid():
                    rental_cart = rental_cart_ser.save()
                else:
                    return Response(CustomError.get_error_by_code("PRC-0", rental_cart_ser.errors),
                                    status=status.HTTP_400_BAD_REQUEST)
            else:
                rental_cart = rental_cart.first()

            rental_cart_item = rental_cart.tools.through.objects.filter(tool_id=tools_model.pk)
            if rental_cart_item.exists():
                rental_cart_item = rental_cart_item.first()
                if rental_cart_item.rental_time != request_data.get('rental_time'):
                    return Response(CustomError.get_error_by_code("PRC-1",
                                                                  {"current": rental_cart_item.rental_time,
                                                                   "new": request_data.get('rental_time')}),
                                    status=status.HTTP_400_BAD_REQUEST, )
                quantity = rental_cart_item.quantity
                rental_cart_item.quantity = quantity + request_data.get('quantity')
                rental_cart_item.save()
                PaymentHelper.update_rental_cart_last_modified(rental_cart)
            else:
                rental_cart.tools.add(tools_model,
                                      through_defaults={"quantity": request_data.get('quantity'),
                                                        "rental_time": request_data.get('rental_time')})

            rental_cart_items = PaymentHelper.get_all_rental_cart_items(rental_cart)
            rental_cart_items_ser = RentalCartItemSerializer(rental_cart_items, many=True)
            return Response(rental_cart_items_ser.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(CustomError.get_error_by_code("GE-0", e), status=status.HTTP_400_BAD_REQUEST)
