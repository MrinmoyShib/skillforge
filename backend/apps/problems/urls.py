"""
URL routing for problems, categories, and tags.
"""
from django.urls import path
from apps.admin_api.apis.problem_views import AdminProblemViewSet
from .apis.views import (
    ProblemListAPI,
    ProblemDetailAPI,
    CategoryListAPI,
    TagListAPI,
)

admin_problem_list = AdminProblemViewSet.as_view({'get': 'list', 'post': 'create'})
admin_problem_detail = AdminProblemViewSet.as_view(
    {'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'},
    lookup_url_kwarg='problem_id'
)

urlpatterns = [
    # Public & Student Endpoints
    path('categories/', CategoryListAPI.as_view(), name='category-list'),
    path('tags/', TagListAPI.as_view(), name='tag-list'),
    path('problems/', ProblemListAPI.as_view(), name='problem-list'),
    path('problems/<slug:slug>/', ProblemDetailAPI.as_view(), name='problem-detail'),

    # Canonical Admin Problem Routes (Delegated to apps.admin_api)
    path('admin/problems/', admin_problem_list, name='admin-problem-list-create'),
    path('admin/problems/<int:problem_id>/', admin_problem_detail, name='admin-problem-detail'),
]

