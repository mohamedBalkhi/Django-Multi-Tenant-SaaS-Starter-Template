"""
Tenant-aware JWT serializers
"""
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class TenantTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom JWT serializer that embeds tenant information in the token
    This ensures tokens are tenant-specific and can't be used across tenants
    """

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Get current tenant from database connection
        from django.db import connection
        tenant_schema = connection.schema_name

        # Embed tenant information in token payload
        token['tenant'] = tenant_schema
        token['username'] = user.username
        token['email'] = user.email

        return token
