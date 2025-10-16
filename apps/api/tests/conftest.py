"""
Pytest fixtures for tenant-aware API testing
"""
import pytest
from django.contrib.auth import get_user_model
from django_tenants.test.cases import TenantTestCase
from django_tenants.test.client import TenantClient
from rest_framework.test import APIClient
from apps.tenants.models import Client, Domain

User = get_user_model()


class APITenantClient(TenantClient, APIClient):
    """
    Custom client that combines TenantClient and APIClient
    Allows testing tenant-specific API endpoints with DRF features
    """
    pass


@pytest.fixture(scope='function')
def tenant(db):
    """
    Create a test tenant
    """
    tenant = Client(
        schema_name='test',
        name='Test Tenant'
    )
    tenant.save()

    domain = Domain(
        domain='test.localhost',
        tenant=tenant,
        is_primary=True
    )
    domain.save()

    return tenant


@pytest.fixture(scope='function')
def api_client(tenant):
    """
    Create a tenant-aware API client
    """
    return APITenantClient(tenant)


@pytest.fixture(scope='function')
def authenticated_client(api_client, tenant):
    """
    Create an authenticated tenant-aware API client
    """
    from django.db import connection
    connection.set_tenant(tenant)

    # Create a test user in the tenant schema
    user = User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpass123'
    )

    api_client.force_authenticate(user=user)
    api_client.user = user

    return api_client
