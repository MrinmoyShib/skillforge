"""
URL routing for code submissions.
"""
from django.urls import path
from .apis.views import SubmissionListCreateAPI, SubmissionDetailAPI

urlpatterns = [
    path('', SubmissionListCreateAPI.as_view(), name='submission-list-create'),
    path('<int:submission_id>/', SubmissionDetailAPI.as_view(), name='submission-detail'),
]

