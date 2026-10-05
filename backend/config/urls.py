from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('apps.core.urls')),
    path('api/v1/auth/', include('apps.accounts.urls')),
    path('api/v1/admin/', include('apps.admin_api.urls')),
    path('api/v1/', include('apps.problems.urls')),
    path('api/v1/submissions/', include('apps.submissions.urls')),
    path('api/v1/progress/', include('apps.progress.urls', namespace='progress')),
    path('api/v1/dashboard/', include('apps.dashboard.urls', namespace='dashboard')),
    path('api/v1/achievements/', include('apps.achievements.urls', namespace='achievements')),
    path('api/v1/leaderboard/', include('apps.leaderboard.urls', namespace='leaderboard')),
    path('api/v1/projects/', include('apps.projects.urls')),
    path('api/v1/portfolio/', include('apps.portfolio.urls')),
]

from rest_framework.permissions import AllowAny, IsAdminUser

doc_permissions = [AllowAny] if settings.DEBUG else [IsAdminUser]

urlpatterns += [
    path('api/schema/', SpectacularAPIView.as_view(permission_classes=doc_permissions), name='schema'),
    path('api/docs/swagger/', SpectacularSwaggerView.as_view(url_name='schema', permission_classes=doc_permissions), name='swagger-ui'),
    path('api/docs/redoc/', SpectacularRedocView.as_view(url_name='schema', permission_classes=doc_permissions), name='redoc'),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
