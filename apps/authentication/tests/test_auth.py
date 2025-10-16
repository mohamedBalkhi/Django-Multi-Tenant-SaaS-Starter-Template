"""
Tests for tenant-aware JWT authentication
"""
import pytest
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken
from apps.core.tests import TenantAPITestCase

User = get_user_model()


@pytest.mark.django_db
class TestTenantJWTAuthentication(TenantAPITestCase):
    """
    Test JWT authentication with tenant isolation
    """

    def setUp(self):
        """Set up test data"""
        super().setUp()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    def test_obtain_jwt_token(self):
        """Test obtaining JWT token"""
        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        response = self.client.post('/api/token/', data)

        assert response.status_code == status.HTTP_200_OK
        assert 'access' in response.data
        assert 'refresh' in response.data

    def test_token_contains_tenant_info(self):
        """Test that JWT token includes tenant information"""
        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        response = self.client.post('/api/token/', data)

        assert response.status_code == status.HTTP_200_OK

        # Decode access token and verify tenant info
        access_token = AccessToken(response.data['access'])
        assert 'tenant' in access_token
        assert access_token['tenant'] == self.tenant.schema_name
        assert access_token['username'] == 'testuser'

    def test_invalid_credentials(self):
        """Test token request with invalid credentials"""
        data = {
            'username': 'testuser',
            'password': 'wrongpassword'
        }
        response = self.client.post('/api/token/', data)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_refresh_token(self):
        """Test refreshing access token"""
        # First, obtain tokens
        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        response = self.client.post('/api/token/', data)
        refresh_token = response.data['refresh']

        # Now refresh
        response = self.client.post('/api/token/refresh/', {'refresh': refresh_token})

        assert response.status_code == status.HTTP_200_OK
        assert 'access' in response.data
