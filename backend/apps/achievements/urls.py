from django.urls import path
from .apis.views import AchievementListAPI

app_name = 'achievements'

urlpatterns = [
    path('', AchievementListAPI.as_view(), name='list'),
]

