"""
Tests for Item API endpoints
"""
import pytest
from django.contrib.auth import get_user_model
from rest_framework import status
from apps.core.tests import TenantAPITestCase
from apps.api.models import Item

User = get_user_model()


@pytest.mark.django_db
class TestItemAPI(TenantAPITestCase):
    """
    Test Item CRUD operations with tenant isolation
    """

    def setUp(self):
        """Set up test data"""
        super().setUp()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)

    def test_create_item(self):
        """Test creating an item"""
        data = {
            'name': 'Test Item',
            'description': 'Test description'
        }
        response = self.client.post('/api/items/', data)

        assert response.status_code == status.HTTP_201_CREATED
        assert Item.objects.count() == 1
        assert Item.objects.first().name == 'Test Item'
        assert Item.objects.first().created_by == self.user

    def test_list_items(self):
        """Test listing items"""
        # Create test items
        Item.objects.create(
            name='Item 1',
            description='Description 1',
            created_by=self.user
        )
        Item.objects.create(
            name='Item 2',
            description='Description 2',
            created_by=self.user
        )

        response = self.client.get('/api/items/')

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 2

    def test_retrieve_item(self):
        """Test retrieving a specific item"""
        item = Item.objects.create(
            name='Test Item',
            description='Test description',
            created_by=self.user
        )

        response = self.client.get(f'/api/items/{item.id}/')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == 'Test Item'

    def test_update_item(self):
        """Test updating an item"""
        item = Item.objects.create(
            name='Original Name',
            description='Original description',
            created_by=self.user
        )

        data = {
            'name': 'Updated Name',
            'description': 'Updated description'
        }
        response = self.client.put(f'/api/items/{item.id}/', data)

        assert response.status_code == status.HTTP_200_OK
        item.refresh_from_db()
        assert item.name == 'Updated Name'

    def test_delete_item(self):
        """Test deleting an item"""
        item = Item.objects.create(
            name='Test Item',
            description='Test description',
            created_by=self.user
        )

        response = self.client.delete(f'/api/items/{item.id}/')

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Item.objects.count() == 0

    def test_unauthenticated_access(self):
        """Test that unauthenticated users can't access endpoints"""
        self.client.force_authenticate(user=None)

        response = self.client.get('/api/items/')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
