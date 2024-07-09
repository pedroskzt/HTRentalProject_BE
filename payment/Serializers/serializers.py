from rest_framework.serializers import ModelSerializer
from payment.models.rental_cart_model import RentalCart, RentalCartItem


class RentalCartSerializer(ModelSerializer):
    class Meta:
        model = RentalCart
        fields = '__all__'


class RentalCartItemSerializer(ModelSerializer):
    class Meta:
        model = RentalCartItem
        fields = '__all__'
