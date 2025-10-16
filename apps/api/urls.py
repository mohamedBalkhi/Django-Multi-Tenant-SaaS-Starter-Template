"""
API URL configuration
"""
from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    # Items endpoints
    path('items/', views.ItemListCreateView.as_view(), name='item-list-create'),
    path('items/<int:pk>/', views.ItemDetailView.as_view(), name='item-detail'),

    # User profile endpoint
    path('profile/', views.UserProfileView.as_view(), name='profile'),
]
