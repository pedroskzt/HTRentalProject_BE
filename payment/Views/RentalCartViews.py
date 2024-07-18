from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from core.PaymentManager.PaymentHandler import PaymentHandler


class AddToolModelToRentalCart(APIView):
    """
    View responsible for adding a tool model to the rental cart.
    """
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)

    def post(self, request):
        return PaymentHandler.handler_add_tool_model_to_cart(request.data, request.user)


class GetRentalCart(APIView):
    """
        View responsible for returning all tool models on the rental cart.
    """
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)

    def get(self, request):
        return PaymentHandler.handler_get_rental_cart(request.user)


class UpdateRentalCart(APIView):
    """
    View responsible for updating user rental cart.
    """
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)

    def post(self, request):
        return PaymentHandler.handler_update_rental_cart(request.data, request.user)
