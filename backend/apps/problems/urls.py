"""
URL routing for problems, categories, tags, and admin problem management.
"""
from django.urls import path
from .apis.views import (
    ProblemListAPI,
    ProblemDetailAPI,
    CategoryListAPI,
    TagListAPI,
)
from .apis.admin_views import (
    AdminProblemListCreateAPI,
    AdminProblemDetailAPI,
    AdminTestCaseListCreateAPI,
    AdminTestCaseDetailAPI,
)

urlpatterns = [
    # Public & Student Endpoints
    path('categories/', CategoryListAPI.as_view(), name='category-list'),
    path('tags/', TagListAPI.as_view(), name='tag-list'),
    path('problems/', ProblemListAPI.as_view(), name='problem-list'),
    path('problems/<slug:slug>/', ProblemDetailAPI.as_view(), name='problem-detail'),

    # Legacy Admin Endpoints (for backwards compatibility with test_problems_api.py)
    path('admin/problems/', AdminProblemListCreateAPI.as_view(), name='admin-problem-list-create'),
    path('admin/problems/<int:problem_id>/', AdminProblemDetailAPI.as_view(), name='admin-problem-detail'),
    path('admin/problems/<int:problem_id>/test-cases/', AdminTestCaseListCreateAPI.as_view(), name='admin-test-case-list-create'),
    path('admin/test-cases/<int:test_case_id>/', AdminTestCaseDetailAPI.as_view(), name='admin-test-case-detail'),
]

