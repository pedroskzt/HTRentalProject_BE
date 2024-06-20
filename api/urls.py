from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from api.Views.ToolsView import GetAllTools

urlpatterns = [
    path('Tools/Get/All', GetAllTools.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
