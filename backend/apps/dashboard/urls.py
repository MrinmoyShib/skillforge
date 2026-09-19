from django.urls import path
from .apis.views import DashboardAPI

app_name = 'dashboard'

urlpatterns = [
    path('', DashboardAPI.as_view(), name='index'),
]

