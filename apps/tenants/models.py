"""
Tenant models for multi-tenancy support
"""
from django.db import models
from django_tenants.models import TenantMixin, DomainMixin


class Client(TenantMixin):
    """
    Tenant model - represents a single tenant/customer
    Each tenant gets their own PostgreSQL schema
    """
    name = models.CharField(max_length=100, help_text="Tenant name (e.g., 'School 1')")
    created_on = models.DateTimeField(auto_now_add=True)
    paid_until = models.DateField(null=True, blank=True, help_text="Subscription end date")
    on_trial = models.BooleanField(default=True, help_text="Is this tenant on trial?")

    # Automatically create and sync schema when tenant is saved
    auto_create_schema = True
    # Safety: prevent accidental schema deletion
    auto_drop_schema = False

    class Meta:
        db_table = 'tenants_client'
        ordering = ['-created_on']

    def __str__(self):
        return f"{self.name} ({self.schema_name})"


class Domain(DomainMixin):
    """
    Domain model - maps domains/subdomains to tenants
    Example: school1.localhost -> tenant with schema 'school1'
    """
    class Meta:
        db_table = 'tenants_domain'

    def __str__(self):
        return f"{self.domain} ({'primary' if self.is_primary else 'secondary'})"
