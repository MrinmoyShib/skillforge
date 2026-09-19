"""
URL routing for Admin API.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .apis.analytics_views import AdminAnalyticsAPI
from .apis.problem_views import AdminProblemViewSet
from .apis.project_views import AdminProjectViewSet
from .apis.user_views import AdminUserViewSet
from .apis.submission_views import AdminSubmissionViewSet

router = DefaultRouter()
router.register(r'problems', AdminProblemViewSet, basename='admin-problems')
router.register(r'projects', AdminProjectViewSet, basename='admin-projects')
router.register(r'users', AdminUserViewSet, basename='admin-users')
router.register(r'submissions', AdminSubmissionViewSet, basename='admin-submissions')

urlpatterns = [
    path('analytics/', AdminAnalyticsAPI.as_view(), name='admin-analytics'),
    path('', include(router.urls)),
]

