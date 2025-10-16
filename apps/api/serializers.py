"""
API serializers
"""
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Item

User = get_user_model()


class ItemSerializer(serializers.ModelSerializer):
    """
    Serializer for Item model
    """
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)

    class Meta:
        model = Item
        fields = ['id', 'name', 'description', 'created_by', 'created_by_username', 'created_at', 'updated_at']
        read_only_fields = ['created_by', 'created_at', 'updated_at']


class UserProfileSerializer(serializers.Serializer):
    """
    Serializer for user profile with tenant context
    """
    id = serializers.IntegerField(source='user.id')
    username = serializers.CharField(source='user.username')
    email = serializers.EmailField(source='user.email')
    tenant_schema = serializers.CharField()
    is_staff = serializers.BooleanField(source='user.is_staff')
    date_joined = serializers.DateTimeField(source='user.date_joined')
