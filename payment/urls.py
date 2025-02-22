from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from payment.Views.CheckoutViews import (GetCheckoutInformation, MakePayment)
from payment.Views.RentalCartViews import (AddToolModelToRentalCart, GetRentalCart, UpdateRentalCart)

urlpatterns = [
    path('RentalCart/Add', AddToolModelToRentalCart.as_view()),
    path('RentalCart/Get', GetRentalCart.as_view()),
    path('RentalCart/Update', UpdateRentalCart.as_view()),
    path('Checkout/Review', GetCheckoutInformation.as_view()),
    path('Checkout/Pay', MakePayment.as_view()),

]

urlpatterns = format_suffix_patterns(urlpatterns)
