from django.urls import path
from .apis.views import LeaderboardAPI

app_name = 'leaderboard'

urlpatterns = [
    path('', LeaderboardAPI.as_view(), name='index'),
]

