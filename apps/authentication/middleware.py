"""
Tenant JWT validation middleware
Ensures tokens can't be used across different tenants
"""
from django.utils.deprecation import MiddlewareMixin
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenError
from django.http import JsonResponse
from django.db import connection


class TenantJWTValidationMiddleware(MiddlewareMixin):
    """
    Middleware to validate that JWT tokens match the current tenant
    Prevents cross-tenant token usage for security
    """

    def process_request(self, request):
        # Skip validation for public schema
        if connection.schema_name == 'public':
            return None

        # Only validate Bearer tokens
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        if not auth_header.startswith('Bearer '):
            return None

        try:
            # Extract and decode token
            token_str = auth_header.split(' ')[1]
            token = AccessToken(token_str)

            # Validate tenant in token matches current tenant
            token_tenant = token.get('tenant')
            current_tenant = connection.schema_name

            if token_tenant != current_tenant:
                return JsonResponse({
                    'error': 'Invalid token for this tenant',
                    'detail': 'This token cannot be used on this domain'
                }, status=403)

        except (TokenError, KeyError, IndexError):
            # Let DRF authentication handle invalid/expired tokens
            pass

        return None
