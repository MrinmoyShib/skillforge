from django.urls import path
from .apis.views import UserProgressSummaryAPI, UserSolvedProblemsAPI

app_name = 'progress'

urlpatterns = [
    path('', UserProgressSummaryAPI.as_view(), name='summary'),
    path('problems/', UserSolvedProblemsAPI.as_view(), name='solved-problems'),
]

