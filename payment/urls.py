from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from payment.Views.RentalCartViews import (AddToolModelToRentalCart)

urlpatterns = [
    path('RentalCart/Add', AddToolModelToRentalCart.as_view()),

]

urlpatterns = format_suffix_patterns(urlpatterns)
