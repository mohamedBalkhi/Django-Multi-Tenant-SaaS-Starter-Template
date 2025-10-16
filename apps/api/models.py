"""
Example API models (tenant-specific)
"""
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Item(models.Model):
    """
    Example model - each tenant has their own isolated items
    Demonstrates tenant isolation at the database level
    """
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='items')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
        ]

    def __str__(self):
        return self.name
