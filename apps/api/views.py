"""
Example API endpoints
"""
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import connection
from .models import Item
from .serializers import ItemSerializer, UserProfileSerializer


class ItemListCreateView(generics.ListCreateAPIView):
    """
    Endpoint 1: List and create items
    GET  /api/items/ - List all items for current tenant
    POST /api/items/ - Create a new item for current tenant

    Items are automatically isolated by tenant schema
    """
    serializer_class = ItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Returns items only from the current tenant's schema
        Automatic tenant isolation via PostgreSQL schemas
        """
        return Item.objects.all()

    def perform_create(self, serializer):
        """
        Automatically set the creator when creating an item
        """
        serializer.save(created_by=self.request.user)


class ItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Endpoint: Retrieve, update, or delete a specific item
    GET    /api/items/<id>/ - Get item details
    PUT    /api/items/<id>/ - Update item
    PATCH  /api/items/<id>/ - Partial update
    DELETE /api/items/<id>/ - Delete item
    """
    serializer_class = ItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Item.objects.all()


class UserProfileView(APIView):
    """
    Endpoint 2: Get current user's profile with tenant context
    GET /api/profile/ - Get user info including current tenant

    Demonstrates how to include tenant information in responses
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """
        Return user profile with tenant context
        """
        serializer = UserProfileSerializer({
            'user': request.user,
            'tenant_schema': connection.schema_name,
        })
        return Response(serializer.data)
