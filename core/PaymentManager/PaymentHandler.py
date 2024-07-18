from django.db.models import Count
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response

from api.Serializers.serializers import LightToolsHistorySerializer
from core.CustomErrors.CustomErrors import CustomError
from core.PaymentManager.PaymentHelper import PaymentHelper
from core.ToolsManager.ToolsHelper import ToolsHelper
from payment.Serializers.serializers import (RentalCartSerializer,
                                             RentalCartItemSerializer,
                                             RentalOrderSerializer,
                                             RentalOrderItemSerializer,
                                             CheckoutSerializer)


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

    @staticmethod
    def handler_get_rental_cart(user):
        try:
            # Check if user has items on the rental cart.
            rental_cart, resp = PaymentHelper.validate_rental_cart(user)
            if resp.status_code != status.HTTP_200_OK:
                return resp

            rental_cart_ser = RentalCartSerializer(rental_cart)
            return Response(rental_cart_ser.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(CustomError.get_error_by_code("GE-0", e), status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def handler_update_rental_cart(request_data, user):
        try:
            # Check if user has items on the rental cart.
            rental_cart, resp = PaymentHelper.validate_rental_cart(user)
            if resp.status_code != status.HTTP_200_OK:
                rental_cart_ser = RentalCartSerializer(data={'user': user.pk})
                if rental_cart_ser.is_valid():
                    rental_cart = rental_cart_ser.save()
                else:
                    return Response(CustomError.get_error_by_code("PRC-0", rental_cart_ser.errors),
                                    status=status.HTTP_400_BAD_REQUEST)

            rental_cart_items = PaymentHelper.get_all_rental_cart_items(rental_cart)
            updated_list = []
            for index, item in enumerate(rental_cart_items.values()):
                tools_model_id = str(item.get('tool_id'))
                if tools_model_id in request_data:
                    data = request_data.get(tools_model_id)
                    if 'quantity' in data and data.get('quantity') == 0:
                        rental_cart_items[index].delete()
                        continue

                    rental_cart_item_ser = RentalCartItemSerializer(instance=rental_cart_items[index], data=data,
                                                                    partial=True)
                    if rental_cart_item_ser.is_valid():
                        updated_list.append(rental_cart_item_ser)
                    else:
                        return Response(CustomError.get_error_by_code("PRC-0", rental_cart_item_ser.errors),
                                        status=status.HTTP_400_BAD_REQUEST)

            for item in updated_list:
                item.save()

            rental_cart_ser = RentalCartSerializer(rental_cart)
            return Response(rental_cart_ser.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(CustomError.get_error_by_code("GE-0", e), status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def handler_get_checkout_information(user):
        """
        Get all information from user cart and uses it to create a RentalOrder. Validates tools requested quantity and
        availability, and return JSON with rental order details.
        :param user: User Object
        :return: JSON RentalOrder serialized
        """
        try:
            # Get user rental cart and check if it exists.
            rental_cart = PaymentHelper.get_rental_cart_by_user(user)
            if rental_cart.exists() is False:
                return Response(CustomError.get_error_by_code("PRC-2", {"User": user}),
                                status=status.HTTP_400_BAD_REQUEST)
            rental_cart = rental_cart.first()

            # Get rental cart items and check if there's any item in the cart.
            rental_cart_items = rental_cart.tools.through.objects.all()
            if rental_cart_items.exists() is False:
                return Response(CustomError.get_error_by_code("PRC-3", {"User": user}),
                                status=status.HTTP_400_BAD_REQUEST)

            # Get all available tools for the models in cart
            models = {}
            for item in rental_cart_items:
                tools_model = item.tool
                models[tools_model.id] = {"tools": list(tools_model.tools_set.filter(available=True)),
                                          "available": item.quantity,
                                          "cart_quantity": item.quantity,
                                          "time_rented": item.rental_time,
                                          "errors": []}
                # Check if quantity requested is available
                if len(models[tools_model.id]['tools']) < item.quantity:
                    if len(models[tools_model.id]['tools']) == 0:
                        models[tools_model.id]['available'] = 0
                        models[tools_model.id]['time_rented'] = 0
                        # models[tools_model.id]['errors'] = ["No more of this tool is available to rent."]
                    else:
                        models[tools_model.id]['available'] = len(models[tools_model.id]['tools'])
                        # models[tools_model.id]['erros'] = [
                        #     f"Only {models[tools_model.id]['quantity']} of this tool are available."]

            # Check if this user has an open rental order and get the latest one. If not, create one.
            rental_order = PaymentHelper.get_rental_orders_by_user(user)
            rental_order = PaymentHelper.validate_rental_order(rental_order)
            if rental_order is False:
                rental_order_ser = RentalOrderSerializer(data={'user': user.pk})
                if rental_order_ser.is_valid():
                    rental_order = rental_order_ser.save()
                else:
                    return Response(CustomError.get_error_by_code("POC-0", rental_order_ser.errors),
                                    status=status.HTTP_400_BAD_REQUEST)

            rental_order_items = rental_order.tools.through.objects.all()
            items_per_model = {}
            for model in rental_order_items.values('tool__model_id').annotate(counter=Count('tool__model_id')):
                items_per_model[model['tool__model_id']] = model['counter']

            quantity_error_msg = {}
            order_data_list = []
            used_tools = []
            for model in models:
                available = models[model]['available']
                cart_quantity = models[model]['cart_quantity']
                tools = models[model]['tools']
                amount_to_add = 0

                if model in items_per_model.keys():
                    if available == 0:
                        if items_per_model[model] == cart_quantity:
                            continue
                        if items_per_model[model] < cart_quantity:
                            quantity_error_msg[
                                model] = f"Not enough tools. There are only {items_per_model[model]} of this tool available."
                            continue

                    if cart_quantity > items_per_model[model]:
                        amount_to_add = cart_quantity - items_per_model[model]
                        amount_to_add = available if amount_to_add > available else amount_to_add

                else:
                    if available == 0:
                        quantity_error_msg[model] = f"This tool is out of stock."
                        continue

                    if available >= cart_quantity:
                        amount_to_add = cart_quantity
                    else:
                        amount_to_add = available
                        quantity_error_msg[
                            model] = f"Not enough tools. There are only {available} of this tool available."

                # Add more tools to the order data list.

                for _ in range(amount_to_add):
                    tool = tools.pop()
                    order_data_list.append({
                        'rental_order': rental_order.pk,
                        'tool': tool.pk,
                        'time_rented': models[model]['time_rented'],
                    })
                    tool.available = False
                    tool.save()
                    used_tools.append(tool)
                    if model in items_per_model.keys():
                        items_per_model[model] += 1
                    else:
                        items_per_model[model] = 1

            rental_order_items_ser = RentalOrderItemSerializer(data=order_data_list, many=True)
            if rental_order_items_ser.is_valid():
                rental_order_items_ser.save()
            else:
                # Failed to serialize rental order items!
                # Undo Changes and Return error
                for tool in used_tools:
                    tool.available = True
                    tool.save()
                return Response(CustomError.get_error_by_code("POC-0", rental_order_items_ser.errors),
                                status=status.HTTP_400_BAD_REQUEST)

            # Double check cart quantity match order quantity and calculate the subtotal.
            rental_order_items = PaymentHelper.get_all_rental_order_items(rental_order)
            rental_order.sub_total = 0

            for model in rental_order_items.values('tool__model_id', 'time_rented', 'tool__model__price').annotate(
                    counter=Count('tool__model_id')):
                model_id = model['tool__model_id']
                counter = model['counter']
                price = model['tool__model__price']
                time_rented = model['time_rented']

                if model_id not in models.keys():
                    cart_quantity = 0
                else:
                    cart_quantity = models[model_id]['cart_quantity']

                if counter > cart_quantity:
                    items = list(rental_order_items.filter(tool__model_id=model_id))
                    for i in range(counter - cart_quantity):
                        item = items.pop()
                        item.tool.available = True
                        item.tool.save()
                        item.delete()
                # Calculate SubTotal
                if cart_quantity > 0:
                    rental_order.sub_total += (cart_quantity * price * time_rented)

            rental_order.save()
            checkout_ser = CheckoutSerializer(rental_order, context={'error_list': quantity_error_msg})
            return Response(checkout_ser.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(CustomError.get_error_by_code("GE-0", e), status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def handler_make_payment(user):
        """
        Concludes the Rental process. Clears the RentalCart, set the RentalOrder as completed
        and create history entries for each tool.
        :param user: User Object
        :return: Status 202
        """
        try:
            # Get user rental order and check if it exists.
            rental_order = PaymentHelper.get_rental_orders_by_user(user)
            if rental_order.exists() is False:
                return Response(CustomError.get_error_by_code("POC-1", {"user": user}),
                                status=status.HTTP_400_BAD_REQUEST)
            rental_order = rental_order.latest('date_created')

            # Log the rental history of the tools.
            tools_rented = []
            for item in rental_order.tools.through.objects.all():
                start_date = timezone.now()
                end_date = timezone.now() + timezone.timedelta(days=item.time_rented)
                tools_rented.append({"tool": item.tool.pk,
                                     "user": user.pk,
                                     "rent_start_date": start_date,
                                     "rent_end_date": end_date})

            tool_history_ser = LightToolsHistorySerializer(data=tools_rented, many=True)
            if tool_history_ser.is_valid():
                tool_history_ser.save()
            else:
                return Response(CustomError.get_error_by_code("TH-0", tool_history_ser.errors),
                                status=status.HTTP_400_BAD_REQUEST)

            # Set the rental order as COMPLETED and the Completion datetime
            rental_order.status = rental_order.COMPLETED
            rental_order.date_completed = timezone.now()
            rental_order.save()

            # Get user rental cart and if still exists, delete it.
            rental_cart = PaymentHelper.get_rental_cart_by_user(user)
            if rental_cart.exists():
                rental_cart.first().delete()

            return Response(status=status.HTTP_202_ACCEPTED)

        except Exception as e:
            return Response(CustomError.get_error_by_code("GE-0", e), status.HTTP_400_BAD_REQUEST)
