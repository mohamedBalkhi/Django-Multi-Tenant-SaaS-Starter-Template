# Django Multi-Tenant SaaS Starter Template

A production-ready Django starter template for building multi-tenant SaaS applications with PostgreSQL schema-based isolation, JWT authentication, and automatic tenant provisioning.

## 🎯 When to Use This Template

**Use this template when building SaaS applications where:**

- ✅ Each **customer/organization needs isolated data** (schools, agencies, companies, teams, stores, etc.)
- ✅ You want **schema-based multi-tenancy** (stronger isolation than row-level filtering)
- ✅ Tenants are **provisioned by admins** (not customer self-signup)
- ✅ Each tenant gets its own **subdomain** (e.g., `customer1.yourdomain.com`)
- ✅ You need **tenant-aware JWT authentication** with cross-tenant protection
- ✅ You want **automatic schema creation** and migration management

**Perfect for:**
- 🏫 School/Education management systems
- 🏢 Agency/Team collaboration platforms
- 🏪 Multi-store e-commerce platforms
- 🏥 Healthcare practice management systems
- 🏗️ Project management tools for multiple organizations
- 🎨 White-label SaaS products
- 🤝 B2B applications with organizational accounts

**What you get out of the box:**
- Complete tenant isolation (each customer = separate PostgreSQL schema)
- Automatic tenant provisioning with initial user account
- Secure JWT authentication that prevents cross-tenant access
- Docker setup for easy development and deployment
- Example REST API endpoints demonstrating tenant isolation
- Comprehensive test suite with tenant-aware testing
- Clean, documented code ready to extend

## ✨ Features

- ✅ **PostgreSQL Schema-Based Multi-Tenancy** - Complete data isolation using `django-tenants`
- ✅ **Tenant-Aware JWT Authentication** - Secure authentication with cross-tenant protection
- ✅ **Admin-Side Tenant Provisioning** - Easy tenant creation via CLI, Admin UI, or API
- ✅ **Automatic Schema Management** - Schemas and migrations created automatically
- ✅ **Hot-Reload Development** - Instant file change detection with Watchdog (no container restarts!)
- ✅ **Docker & Docker Compose** - Production-ready containerization with dev-optimized workflow
- ✅ **Makefile Commands** - Simple `make` commands for common tasks
- ✅ **Enhanced Dev Tools** - django-extensions with shell_plus, runserver_plus, and more
- ✅ **REST API with DRF** - Example endpoints demonstrating tenant isolation
- ✅ **Comprehensive Test Suite** - pytest tests with tenant isolation coverage
- ✅ **Easy to Extend** - Clean architecture, well-documented code

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│  Public Schema (localhost:8000)                         │
│  - Admin Interface                                       │
│  - Tenant Management                                     │
└─────────────────────────────────────────────────────────┘

┌─────────────────────┐  ┌─────────────────────┐
│  Tenant 1 Schema    │  │  Tenant 2 Schema    │
│  (school1.localhost)│  │  (school2.localhost)│
│  - Isolated Data    │  │  - Isolated Data    │
│  - JWT Auth         │  │  - JWT Auth         │
│  - API Endpoints    │  │  - API Endpoints    │
└─────────────────────┘  └─────────────────────┘
```

Each tenant gets:
- **Dedicated PostgreSQL schema** (automatic creation)
- **Isolated database tables** (automatic migration)
- **Subdomain routing** (e.g., `tenant1.localhost:8000`)
- **Tenant-specific JWT tokens** (cross-tenant protection)

**Smart Domain Handling:**
- Unmapped domains (like `localhost`) automatically fall back to the public schema
- No manual setup required for admin panel access
- Fresh installations work immediately without domain configuration

## 🚀 Quick Start

### Prerequisites

- Python 3.12+
- PostgreSQL 14+ (or use Docker)
- Docker & Docker Compose (optional, recommended)

### Option 1: Docker (Recommended) ⚡

**With auto-reload enabled - changes to your code are instantly reflected!**

```bash
# 1. Clone and navigate to directory
cd DjangoMultiTenancy

# 2. Copy environment file (already exists, but check settings)
cp .env.example .env  # Optional: modify if needed

# 3. Start services with auto-reload (using Makefile - recommended)
make docker-up

# Or manually:
docker-compose up --build

# 4. Create demo tenants (includes test users)
docker-compose exec web python manage.py setup_demo

# 5. (Optional) Create a superuser for Django admin panel
docker-compose exec -it web python manage.py createsuperuser
```

**That's it! 🎉 Your multi-tenant app is running with hot-reload!**

**🔥 Development Features:**
- ✅ **Auto-reload** - File changes instantly reload the server (powered by Watchdog)
- ✅ **Enhanced shell** - Use `make docker-shell` for shell_plus with auto-imports
- ✅ **Live logs** - Use `make docker-logs` to follow server logs in real-time
- ✅ **Volume mounts** - Code changes sync immediately without rebuilds

> **📝 Note**: Migration files are **already included** in the repository. The `docker-compose up` command automatically applies them to create the database schema. You only need to create new migrations if you add/modify models later (see "Adding New Code/Migrations" section below).

**Access Points:**
- **School 1 API**: http://school1.localhost:8000/api/
- **School 2 API**: http://school2.localhost:8000/api/
- **Admin Panel**: http://localhost:8000/admin (after creating superuser)

**Demo Credentials** (for both tenants):
- Username: `demo`
- Password: `demo123`

### Option 2: Local Development

**Prerequisites:** PostgreSQL must be installed and running locally.

```bash
# 1. Create virtual environment with Python 3.12
python3.12 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure database connection
cp .env.example .env
# Edit .env and update POSTGRES_HOST=localhost (and credentials if needed)

# 4. Run migrations for public schema (creates tenant tables)
POSTGRES_HOST=localhost python manage.py migrate_schemas --shared

# 5. Create demo tenants (automatically runs tenant migrations)
python manage.py setup_demo

# 6. (Optional) Create superuser for admin panel (created in public schema)
python manage.py createsuperuser

# 7. Run development server
python manage.py runserver
```

> **📝 Note**: Migration files are already in the repo. The commands above **apply** existing migrations to your local database. You don't need to create migrations unless you're adding new models.

**Access Points:**
- School 1: http://school1.localhost:8000/api/
- School 2: http://school2.localhost:8000/api/
- Admin: http://localhost:8000/admin

## 🏢 Creating Tenants

Tenants are created **by admins only** (not customer self-signup). When you provision a new tenant, you get:
- ✅ Isolated PostgreSQL schema
- ✅ Subdomain mapping
- ✅ Initial admin/manager user account (optional but recommended)

### Method 1: Management Command (CLI) - Recommended

**With initial user (recommended for production):**
```bash
python manage.py create_tenant \
  --schema=acmecorp \
  --name="ACME Corporation" \
  --domain=acmecorp.yourdomain.com \
  --admin-username=admin \
  --admin-email=admin@acmecorp.com
# Will prompt for password securely
```

**Quick setup (password in command - for dev/testing only):**
```bash
python manage.py create_tenant \
  --schema=school1 \
  --name="School 1" \
  --domain=school1.localhost \
  --admin-username=manager \
  --admin-email=manager@school1.com \
  --admin-password=temppass123
```

**Minimal (just schema + domain, no user):**
```bash
python manage.py create_tenant \
  --schema=school1 \
  --name="School 1" \
  --domain=school1.localhost
# You'll need to create users manually later
```

**What happens automatically:**
1. ✅ Creates PostgreSQL schema (e.g., `acmecorp`)
2. ✅ Runs all migrations for the schema
3. ✅ Creates domain mapping (e.g., `acmecorp.yourdomain.com`)
4. ✅ Creates initial admin user (if `--admin-*` flags provided)
5. ✅ Tenant ready to use immediately!

### Method 2: Django Admin UI

1. Go to http://localhost:8000/admin
2. Click "Clients" → "Add Client"
3. Fill in:
   - **Schema name**: `school1`
   - **Name**: `School 1`
4. Save (schema automatically created)
5. Click "Domains" → "Add Domain"
6. Fill in:
   - **Domain**: `school1.localhost`
   - **Tenant**: Select "School 1"
   - **Is primary**: ✓
7. Save

**Done!** Access at http://school1.localhost:8000

⚠️ **Note:** This method only creates the schema and domain. You'll need to create the initial user manually (see "Creating a User for a Tenant" section below).

### Method 3: Programmatic (Python)

```python
from apps.tenants.models import Client, Domain
from django.contrib.auth import get_user_model
from django.db import connection

User = get_user_model()

# Create tenant (automatic schema creation!)
tenant = Client.objects.create(
    schema_name='school1',
    name='School 1',
    on_trial=True
)

# Create domain
Domain.objects.create(
    domain='school1.localhost',
    tenant=tenant,
    is_primary=True
)

# Create initial admin user for this tenant
connection.set_tenant(tenant)
user = User.objects.create_user(
    username='admin',
    email='admin@school1.com',
    password='secure_password_here'
)
connection.set_schema_to_public()  # Switch back
```

**Tip:** Use the management command (Method 1) for consistent tenant provisioning with built-in validation and user creation.

## ⚡ Development Workflow

### Using Makefile Commands (Recommended)

The template includes a comprehensive Makefile with helpful development commands:

```bash
# View all available commands
make help

# Docker development (with auto-reload)
make docker-up          # Start containers with hot-reload
make docker-down        # Stop containers
make docker-logs        # Follow logs in real-time
make docker-rebuild     # Rebuild from scratch
make docker-shell       # Open enhanced Django shell in container

# Local development
make run                # Run development server with auto-reload
make shell              # Open Django shell
make shell-plus         # Open enhanced shell with auto-imports
make migrate            # Run migrations for all tenants

# Testing
make test               # Run test suite
make test-cov           # Run tests with coverage report

# Database management
make demo               # Create demo tenants
make superuser          # Create superuser for admin

# Maintenance
make clean              # Clean Python cache files
```

### Hot-Reload Development Experience

**Docker:** The development server uses `runserver_plus` with Watchdog for instant file change detection:
- Edit Python files → Server reloads automatically
- Edit templates → Changes reflect immediately
- No need to restart containers

**Local:** Same hot-reload experience with `make run`

## 📝 Adding New Code/Migrations

When you add new models or make changes:

```bash
# Create migration
python manage.py makemigrations

# Apply to ALL tenants automatically
python manage.py migrate_schemas

# Or using Makefile
make migrate
```

This updates:
- Public schema
- All existing tenant schemas
- Future tenant schemas (automatic on creation)

## 🔐 Authentication

### Getting JWT Tokens

```bash
# Request token for a tenant
curl -X POST http://school1.localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "demo",
    "password": "demo123"
  }'

# Response:
{
  "access": "eyJ0eXAiOiJKV1QiLC...",
  "refresh": "eyJ0eXAiOiJKV1QiLC..."
}
```

The access token includes:
- User ID and username
- **Tenant schema** (security: prevents cross-tenant usage)
- Expiration: 15 minutes

### Using Tokens

```bash
curl http://school1.localhost:8000/api/items/ \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLC..."
```

### Refreshing Tokens

```bash
curl -X POST http://school1.localhost:8000/api/token/refresh/ \
  -H "Content-Type: application/json" \
  -d '{
    "refresh": "eyJ0eXAiOiJKV1QiLC..."
  }'
```

## 📡 Example API Endpoints

All endpoints are tenant-specific (automatically isolated):

### Items API

```bash
# List items (tenant-specific)
GET /api/items/

# Create item
POST /api/items/
{
  "name": "My Item",
  "description": "Item description"
}

# Get specific item
GET /api/items/{id}/

# Update item
PUT /api/items/{id}/
PATCH /api/items/{id}/

# Delete item
DELETE /api/items/{id}/
```

### User Profile

```bash
# Get current user profile with tenant context
GET /api/profile/

# Response:
{
  "id": 1,
  "username": "demo",
  "email": "demo@school1.com",
  "tenant_schema": "school1",
  "is_staff": false,
  "date_joined": "2025-10-15T10:30:00Z"
}
```

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=apps --cov-report=html

# Run specific test file
pytest apps/api/tests/test_items.py

# Run specific test
pytest apps/api/tests/test_items.py::TestItemAPI::test_create_item
```

View coverage report: Open `htmlcov/index.html` in browser

## 🔧 Extending the Template

This template provides the **multi-tenancy infrastructure**. You'll build your business logic on top of it.

### Common Extensions You'll Add

**For a School Management System:**
- User roles (manager, teacher, student, parent)
- Permission system (who can create/view what)
- Business models (Course, Class, Assignment, Grade, etc.)
- User management endpoints (manager creates teachers/students)

**For a Team Collaboration Tool:**
- User roles (owner, admin, member, guest)
- Permission system and feature access
- Business models (Project, Task, Comment, File, etc.)
- Team member invitation system

**For a Multi-Store E-commerce Platform:**
- User roles (store owner, staff, customer)
- Permission system for store management
- Business models (Product, Order, Customer, Invoice, etc.)
- Store staff management

The template gives you: **tenant isolation + JWT auth + initial user**
You add: **roles + permissions + business models + workflows**

---

### Adding a New Tenant-Specific Model

1. **Create model in `apps/api/models.py`** (or create new app)

```python
class Course(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
```

2. **Add to TENANT_APPS** in `config/settings/base.py`

```python
TENANT_APPS = (
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'apps.api',  # Already there
    # 'apps.courses',  # If you created a new app
)
```

3. **Create and apply migrations**

```bash
python manage.py makemigrations
python manage.py migrate_schemas  # Updates all tenants!
```

### Adding a New API Endpoint

1. **Create view in `apps/api/views.py`**

```python
class CourseListView(generics.ListAPIView):
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Course.objects.all()  # Auto tenant-filtered!
```

2. **Add route in `apps/api/urls.py`**

```python
urlpatterns = [
    path('courses/', views.CourseListView.as_view()),
    # ... existing routes
]
```

3. **Test it!**

```bash
curl http://school1.localhost:8000/api/courses/ \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## 📁 Project Structure

```
DjangoMultiTenancy/
├── apps/
│   ├── tenants/              # Tenant management
│   │   ├── models.py         # Client & Domain models
│   │   ├── admin.py          # Admin interface
│   │   └── management/commands/
│   │       ├── create_tenant.py
│   │       └── setup_demo.py
│   ├── authentication/       # JWT auth
│   │   ├── serializers.py    # Tenant-aware tokens
│   │   ├── middleware.py     # Cross-tenant protection
│   │   └── views.py
│   └── api/                  # Example endpoints
│       ├── models.py         # Item model
│       ├── views.py          # API views
│       ├── serializers.py
│       └── tests/
├── config/
│   ├── settings/
│   │   ├── base.py           # Shared settings
│   │   ├── development.py
│   │   └── production.py
│   ├── urls.py               # Tenant URLs
│   └── urls_public.py        # Public schema URLs
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md
```

## 🌐 Production Deployment

### DNS Configuration

For production, configure a wildcard DNS record:

```
*.yourdomain.com  →  YOUR_SERVER_IP
```

This allows all subdomains to work automatically:
- `tenant1.yourdomain.com`
- `tenant2.yourdomain.com`
- etc.

### Environment Variables

Update `.env` for production:

```env
DJANGO_SECRET_KEY=your-very-secure-secret-key-here
DJANGO_DEBUG=False
DJANGO_SETTINGS_MODULE=config.settings.production
DJANGO_ALLOWED_HOSTS=.yourdomain.com,yourdomain.com

POSTGRES_DB=production_db
POSTGRES_USER=produser
POSTGRES_PASSWORD=secure-password-here
POSTGRES_HOST=your-db-host
POSTGRES_PORT=5432

CORS_ALLOWED_ORIGINS=https://yourdomain.com,https://app.yourdomain.com
```

### Security Checklist

- [ ] Change `SECRET_KEY` to a random value
- [ ] Set `DEBUG=False`
- [ ] Configure `ALLOWED_HOSTS` properly
- [ ] Use HTTPS (configure reverse proxy like Nginx)
- [ ] Set up proper database backups
- [ ] Configure firewall rules
- [ ] Review `config/settings/production.py` settings
- [ ] Set up monitoring and logging

## 🛠️ Common Tasks

### Creating a User for a Tenant

**Option 1: During tenant creation (recommended)**
```bash
# Create tenant with initial user in one command
python manage.py create_tenant \
  --schema=school1 \
  --name="School 1" \
  --domain=school1.localhost \
  --admin-username=manager \
  --admin-email=manager@school1.com
# Will prompt for password
```

**Option 2: Add user to existing tenant**
```bash
# Switch to tenant and create user
python manage.py shell

from django.contrib.auth import get_user_model
from apps.tenants.models import Client
from django.db import connection

# Get tenant
tenant = Client.objects.get(schema_name='school1')
connection.set_tenant(tenant)

# Create user
User = get_user_model()
user = User.objects.create_user(
    username='john',
    email='john@school1.com',
    password='secure123'
)

# Remember to switch back to public schema
connection.set_schema_to_public()
```

**💡 Pro Tip:** In your actual SaaS application, you'd build an API endpoint that allows the initial admin user to create additional users for their tenant (team members, students, etc.). The template provides the foundation - you add the business-specific user management logic.

### Listing All Tenants

```bash
python manage.py shell

from apps.tenants.models import Client
for tenant in Client.objects.all():
    print(f"{tenant.name}: {tenant.schema_name} -> {tenant.domains.first().domain}")
```

### Deleting a Tenant

```bash
python manage.py shell

from apps.tenants.models import Client
tenant = Client.objects.get(schema_name='school1')
tenant.delete()  # WARNING: Deletes the schema and ALL data!
```

## 🤝 Contributing

This is a starter template. Feel free to:
- Fork and customize for your needs
- Report issues or suggestions
- Submit pull requests with improvements

## 📄 License

This project is open source and available under the MIT License.

## 💡 Tips & Best Practices

1. **Always test tenant isolation** - Ensure data doesn't leak between tenants
2. **Use management commands** - Automate tenant provisioning with `create_tenant` for consistency
3. **Create initial admin user** - Always provision tenants with `--admin-*` flags for production
4. **Build user management** - Add API endpoints for the initial admin to create team members/users
5. **Monitor schema count** - Large numbers of schemas may need optimization
6. **Backup strategies** - Consider per-tenant backup schedules
7. **Logging** - Use tenant context in logs (already configured)
8. **Performance** - Add indexes on frequently queried fields
9. **Testing** - Write tests for new features using `TenantTestCase`
10. **Business logic** - The template provides multi-tenancy infrastructure; you add roles, permissions, and business-specific features

## 🆘 Troubleshooting

### "No tenant for hostname" error
**This should NOT happen** - the template automatically falls back to the public schema for unmapped domains.

If you see this error:
1. Check that `SHOW_PUBLIC_IF_NO_TENANT_FOUND = True` is set in `config/settings/base.py`
2. This setting ensures `localhost` and any new domain automatically serves the admin panel
3. You don't need to manually create domain mappings for localhost or admin access

**How it works:**
- When you access an unmapped domain (like `localhost` or a new domain), the system automatically uses the public schema
- This means `/admin` and public URLs work immediately without setup
- Only tenant-specific subdomains need explicit domain mappings

### "relation does not exist" error
Run migrations: `python manage.py migrate_schemas`

### Can't access tenant subdomain locally
Make sure you're using `.localhost` (works automatically). For other domains, edit `/etc/hosts`

### Migrations not applying to tenants
Use `migrate_schemas` instead of `migrate`

### Docker database connection errors
Check if PostgreSQL is healthy: `docker-compose ps`

## 📚 Learn More

- [django-tenants Documentation](https://django-tenants.readthedocs.io/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Simple JWT](https://django-rest-framework-simplejwt.readthedocs.io/)
- [Docker Documentation](https://docs.docker.com/)

---

**Built with ❤️ for building great SaaS applications**
