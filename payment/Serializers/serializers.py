from django.db.models import Count
from rest_framework.serializers import ModelSerializer, SerializerMethodField

from payment.models.rental_cart_model import RentalCart, RentalCartItem
from payment.models.rental_order_model import RentalOrder, RentalOrderItem


class RentalCartSerializer(ModelSerializer):
    class Meta:
        model = RentalCart
        fields = '__all__'


class RentalCartItemSerializer(ModelSerializer):
    class Meta:
        model = RentalCartItem
        fields = '__all__'


class RentalOrderSerializer(ModelSerializer):
    class Meta:
        model = RentalOrder
        fields = '__all__'


class RentalOrderItemSerializer(ModelSerializer):
    class Meta:
        model = RentalOrderItem
        fields = '__all__'


class CheckoutSerializer(ModelSerializer):
    tools_models = SerializerMethodField()

    def get_tools_models(self, obj):
        error_list = self.context.get('error_list')
        tools_models = obj.tools.through.objects.all().values("tool__model_id", "time_rented").annotate(
            quantity=Count("tool__model_id"))

        if error_list:
            for model in tools_models:
                model_id = model["tool__model_id"]
                model["error_msg"] = error_list[model_id]

            if tools_models.exists() is False:
                return [{"tool__model_id": model_id,
                         "error_msg": error_list[model_id],
                         "time_rented": None,
                         "quantity": None} for model_id in error_list]

        return tools_models

    class Meta:
        model = RentalOrder
        fields = '__all__'
