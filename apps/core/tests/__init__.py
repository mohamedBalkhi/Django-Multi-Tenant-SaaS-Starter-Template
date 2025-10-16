"""
Base test classes for multi-tenant API testing

This module provides base test classes that combine django-tenants
with Django REST Framework for clean, scalable API testing.
"""
from django_tenants.test.cases import TenantTestCase
from rest_framework.test import APIClient


class TenantAPITestCase(TenantTestCase):
    """
    Base test case for tenant-aware API testing

    Combines django-tenants' TenantTestCase with DRF's APIClient to provide:
    - Automatic tenant isolation for each test
    - Full DRF test client functionality (force_authenticate, etc.)
    - Clean inheritance pattern for all API tests

    Usage:
        class TestMyAPI(TenantAPITestCase):
            def setUp(self):
                super().setUp()
                self.user = User.objects.create_user(username='test', password='test')
                self.client.force_authenticate(user=self.user)

            def test_my_endpoint(self):
                response = self.client.get('/api/endpoint/')
                assert response.status_code == 200

    Note:
        - Each test automatically gets a fresh tenant schema
        - self.tenant is available with the current test tenant
        - self.client is DRF's APIClient with all authentication helpers
        - Requests are automatically routed to the test tenant domain
    """
    client_class = APIClient

    def _fixture_setup(self):
        """
        Set up test fixtures and configure APIClient for tenant routing
        """
        super()._fixture_setup()
        # Configure client to route requests to the test tenant domain
        self.client = self.client_class(SERVER_NAME=self.get_test_tenant_domain())
