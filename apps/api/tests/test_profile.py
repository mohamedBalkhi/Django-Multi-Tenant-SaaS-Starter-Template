"""
Tests for User Profile API endpoint
"""
import pytest
from django.contrib.auth import get_user_model
from rest_framework import status
from apps.core.tests import TenantAPITestCase

User = get_user_model()


@pytest.mark.django_db
class TestUserProfileAPI(TenantAPITestCase):
    """
    Test user profile endpoint with tenant context
    """

    def setUp(self):
        """Set up test data"""
        super().setUp()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)

    def test_get_profile(self):
        """Test retrieving user profile"""
        response = self.client.get('/api/profile/')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['username'] == 'testuser'
        assert response.data['email'] == 'test@example.com'
        assert 'tenant_schema' in response.data

    def test_profile_includes_tenant_context(self):
        """Test that profile includes current tenant information"""
        response = self.client.get('/api/profile/')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['tenant_schema'] == self.tenant.schema_name

    def test_unauthenticated_profile_access(self):
        """Test that unauthenticated users can't access profile"""
        self.client.force_authenticate(user=None)

        response = self.client.get('/api/profile/')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
