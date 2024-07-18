from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from core.PaymentManager.PaymentHandler import PaymentHandler


class GetCheckoutInformation(APIView):
    """
    View responsible creating the rental order and return the checkout information.
    """
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)

    def post(self, request):
        return PaymentHandler.handler_get_checkout_information(request.user)


class MakePayment(APIView):
    """
    View responsible concluding the rent process and handling payment request.
    """
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)

    def post(self, request):
        return PaymentHandler.handler_make_payment(request.user)
