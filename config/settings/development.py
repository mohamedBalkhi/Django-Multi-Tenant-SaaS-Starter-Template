"""
Development settings
"""
from .base import *

DEBUG = True

# Allow all localhost variations for development
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '.localhost']

# Development-specific CORS settings
CORS_ALLOW_ALL_ORIGINS = True

# Show SQL queries in development
LOGGING['loggers']['django.db.backends'] = {
    'handlers': ['console'],
    'level': 'DEBUG',
    'propagate': False,
}
