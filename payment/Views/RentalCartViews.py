from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
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