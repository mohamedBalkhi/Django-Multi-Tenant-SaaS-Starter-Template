"""
Authentication views
"""
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import TenantTokenObtainPairSerializer


class TenantTokenObtainPairView(TokenObtainPairView):
    """
    Custom token view that uses our tenant-aware serializer
    """
    serializer_class = TenantTokenObtainPairSerializer
