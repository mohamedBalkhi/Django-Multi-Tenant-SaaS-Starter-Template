"""
Main URL configuration (for tenant schemas)
This is used for all tenant-specific requests
"""
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from apps.authentication.views import TenantTokenObtainPairView

urlpatterns = [
    # JWT Authentication endpoints
    path('api/token/', TenantTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # API endpoints
    path('api/', include('apps.api.urls')),
]
