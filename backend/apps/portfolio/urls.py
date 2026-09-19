"""
URL routing for Public Developer Portfolios.
"""
from django.urls import path
from .apis.views import PublicPortfolioAPI

urlpatterns = [
    path('<str:username>/', PublicPortfolioAPI.as_view(), name='public-portfolio'),
]

