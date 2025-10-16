# Contributing to Django Multi-Tenant SaaS Template

Thank you for considering contributing to this project! This document provides guidelines for extending and customizing the template.

## Getting Started

1. **Fork the repository**
2. **Clone your fork**
   ```bash
   git clone https://github.com/YOUR_USERNAME/DjangoMultiTenancy.git
   cd DjangoMultiTenancy
   ```
3. **Set up development environment**
   ```bash
   ./scripts/quickstart.sh
   ```

## Development Workflow

### Adding New Features

1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Write clean, documented code
   - Follow Django best practices
   - Add type hints where beneficial
   - Update README if needed

3. **Add tests**
   - All new features should have tests
   - Use `TenantTestCase` for tenant-specific features
   - Aim for >80% coverage

4. **Run tests**
   ```bash
   pytest
   ```

5. **Check code quality**
   ```bash
   python manage.py check
   ```

### Code Style

- Follow PEP 8
- Use meaningful variable names
- Add docstrings to functions and classes
- Keep functions focused and small
- Comment complex logic

### Testing Guidelines

```python
# Good test structure
@pytest.mark.django_db
class TestFeature(TenantTestCase):
    def setUp(self):
        """Set up test data"""
        super().setUp()
        # Setup code

    def test_specific_behavior(self):
        """Test description"""
        # Arrange
        # Act
        # Assert
```

## Adding New Apps

1. **Create app structure**
   ```bash
   mkdir -p apps/yourapp
   cd apps/yourapp
   # Create necessary files
   ```

2. **Add to TENANT_APPS or SHARED_APPS**
   ```python
   # In config/settings/base.py
   TENANT_APPS = (
       # ...
       'apps.yourapp',
   )
   ```

3. **Create models, views, tests**

4. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate_schemas
   ```

## Tenant Isolation Best Practices

1. **Always test tenant isolation**
   ```python
   def test_tenant_isolation(self):
       # Create data in tenant1
       # Switch to tenant2
       # Verify data from tenant1 is not visible
   ```

2. **Never bypass django-tenants**
   - Don't use raw SQL that ignores schemas
   - Always use Django ORM

3. **Test cross-tenant token protection**
   - Ensure JWT tokens don't work across tenants

## Common Patterns

### Adding a Tenant-Specific Model

```python
# apps/yourapp/models.py
from django.db import models

class YourModel(models.Model):
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
```

### Adding an API Endpoint

```python
# apps/yourapp/views.py
from rest_framework import generics, permissions
from .models import YourModel
from .serializers import YourModelSerializer

class YourModelListView(generics.ListCreateAPIView):
    serializer_class = YourModelSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return YourModel.objects.all()  # Auto tenant-filtered!
```

### Adding a Management Command

```python
# apps/yourapp/management/commands/your_command.py
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Description of your command'

    def handle(self, *args, **options):
        # Your logic here
        self.stdout.write(self.style.SUCCESS('Success!'))
```

## Documentation

- Update README.md for user-facing changes
- Update IMPLEMENTATION_PLAN.md for architectural changes
- Add inline comments for complex logic
- Write clear commit messages

## Commit Messages

Use clear, descriptive commit messages:

```
feat: Add Course model and API endpoints
fix: Resolve tenant isolation issue in Item queryset
docs: Update README with deployment guide
test: Add tests for JWT token validation
refactor: Simplify tenant creation logic
```

## Pull Requests

1. Ensure all tests pass
2. Update documentation
3. Add a clear description of changes
4. Reference any related issues

## Questions?

Open an issue for:
- Bug reports
- Feature requests
- Questions about implementation
- Clarifications needed

Thank you for contributing! 🎉
