"""
Admin interface for tenant management
"""
from django.contrib import admin
from django_tenants.admin import TenantAdminMixin
from .models import Client, Domain


@admin.register(Client)
class ClientAdmin(TenantAdminMixin, admin.ModelAdmin):
    """
    Admin interface for managing tenants
    """
    list_display = ['name', 'schema_name', 'created_on', 'on_trial', 'paid_until']
    search_fields = ['name', 'schema_name']
    list_filter = ['on_trial', 'created_on']
    readonly_fields = ['created_on', 'schema_name']

    fieldsets = (
        ('Basic Information', {
            'fields': ('schema_name', 'name', 'created_on')
        }),
        ('Subscription', {
            'fields': ('on_trial', 'paid_until')
        }),
    )


@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    """
    Admin interface for managing tenant domains
    """
    list_display = ['domain', 'tenant', 'is_primary']
    list_filter = ['is_primary']
    search_fields = ['domain', 'tenant__name', 'tenant__schema_name']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('tenant')
