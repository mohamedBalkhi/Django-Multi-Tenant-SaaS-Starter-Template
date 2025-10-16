"""
Public schema URL configuration
These URLs are accessible on the main domain (not tenant subdomains)
"""
from django.contrib import admin
from django.urls import path
from django.http import JsonResponse


def health_check(request):
    """Simple health check endpoint for Docker/monitoring"""
    return JsonResponse({'status': 'ok', 'message': 'Django multi-tenant app is running'})


def home(request):
    """Simple home page for the public schema"""
    return JsonResponse({
        'message': 'Welcome to Django Multi-Tenant SaaS Template',
        'version': '1.0.0',
        'admin': '/admin/',
        'health': '/health/',
    })


urlpatterns = [
    # Admin interface (only on public schema)
    path('admin/', admin.site.urls),

    # Health check endpoint
    path('health/', health_check, name='health_check'),

    # Home
    path('', home, name='home'),
]
