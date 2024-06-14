from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from api_auth.User.UserView import (UserLogin)

urlpatterns = [
    path('Login', UserLogin.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)