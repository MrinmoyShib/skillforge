"""
URL routing for Guided Projects and Milestones.
"""
from django.urls import path
from .apis.views import (
    ProjectListAPI,
    ProjectDetailAPI,
    ProjectStartAPI,
    MilestoneVerifyAPI,
)

urlpatterns = [
    path('', ProjectListAPI.as_view(), name='project-list'),
    path('<slug:slug>/', ProjectDetailAPI.as_view(), name='project-detail'),
    path('<slug:slug>/start/', ProjectStartAPI.as_view(), name='project-start'),
    path('<slug:slug>/milestones/<int:milestone_id>/verify/', MilestoneVerifyAPI.as_view(), name='milestone-verify'),
]

