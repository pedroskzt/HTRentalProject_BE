from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from payment.Views.RentalCartViews import (AddToolModelToRentalCart)
from payment.Views.CheckoutViews import (GetCheckoutInformation, MakePayment)

urlpatterns = [
    path('RentalCart/Add', AddToolModelToRentalCart.as_view()),
    path('Checkout/Review', GetCheckoutInformation.as_view()),
    path('Checkout/Pay', MakePayment.as_view()),

]

urlpatterns = format_suffix_patterns(urlpatterns)