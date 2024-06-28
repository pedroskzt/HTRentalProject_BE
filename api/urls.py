from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from api.Views.ToolsView import (GetAllTools,
                                 GetAllToolsModels,
                                 GetTool,
                                 GetToolsByCategory,
                                 GetToolsHistoryByUser
                                 )

urlpatterns = [
    path('Tools/Get/All', GetAllTools.as_view()),
    path('Tools/Models/Get/All', GetAllToolsModels.as_view()),
    path('tools/<int:tool_id>', GetTool.as_view(), name='get_tool_by_id'),
    path('tools/category/', GetToolsByCategory.as_view()),
    path('Tools/History/Get/ByUser', GetToolsHistoryByUser.as_view()),

]

urlpatterns = format_suffix_patterns(urlpatterns)
