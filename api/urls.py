from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from api.Views.ToolsView import (GetAllTools,
                                 GetAllToolsModels,
                                 GetToolsModelById,
                                 GetTool,
                                 GetToolsByCategory,
                                 GetToolsHistoryByUser,
                                 GetAllCategories,
                                 AddTool,
                                 UpdateTool
                                 )
from api.Views.ChatBotViews import GetChatBotResponse

urlpatterns = [
    path('Tools/Models/Get/All', GetAllToolsModels.as_view()),
    path('Tools/Models/Get/<int:model_id>', GetToolsModelById.as_view()),
    path('Tools/Models/Get/ByCategory/<int:category_id>', GetToolsByCategory.as_view()),
    path('Tools/Get/All', GetAllTools.as_view()),
    path('Tools/Get/<int:tool_id>', GetTool.as_view(), name='get_tool_by_id'),
    path('Tools/History/Get/ByUser', GetToolsHistoryByUser.as_view()),
    path('Tools/Category/Get/All', GetAllCategories.as_view()),
    path('Tools/Add', AddTool.as_view()),
    path('Tools/Update/<int:tool_id>', UpdateTool.as_view()),
    path('ChatBot/Input', GetChatBotResponse.as_view())

]

urlpatterns = format_suffix_patterns(urlpatterns)
