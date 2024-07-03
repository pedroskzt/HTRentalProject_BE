from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from api_auth.User.UserView import (UserLogin, UserRegistration, UserUpdate, UserGetInfo, ChangePassword)

urlpatterns = [
    path('Login', UserLogin.as_view()),
    path('registration', UserRegistration.as_view()),
    path('User/Update', UserUpdate.as_view()),
    path('User/Get/Info', UserGetInfo.as_view()),
    path('ChangePassword', ChangePassword.as_view())
]
urlpatterns = format_suffix_patterns(urlpatterns)
