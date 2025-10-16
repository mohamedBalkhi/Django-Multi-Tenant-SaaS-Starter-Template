"""
Management command to create demo tenants for testing
Usage: python manage.py setup_demo
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.tenants.models import Client, Domain
from django.db import connection

User = get_user_model()


class Command(BaseCommand):
    help = 'Create demo tenants with sample data for testing'

    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_HEADING('Setting up demo tenants...\n'))

        # First, ensure public tenant exists for localhost/admin access
        public_tenant = Client.objects.filter(schema_name='public').first()
        if not public_tenant:
            self.stdout.write('📦 Creating public tenant for admin access...')
            public_tenant = Client(
                schema_name='public',
                name='Public',
                on_trial=False
            )
            # Don't auto-create schema since 'public' already exists in PostgreSQL
            public_tenant.auto_create_schema = False
            public_tenant.save()

            # Create localhost domain for admin panel access
            Domain.objects.create(
                domain='localhost',
                tenant=public_tenant,
                is_primary=True
            )
            self.stdout.write(
                self.style.SUCCESS('✅ Public tenant created for http://localhost:8000/admin\n')
            )
        else:
            self.stdout.write(
                self.style.WARNING('⚠️  Public tenant already exists, skipping...\n')
            )

        demo_tenants = [
            {
                'schema': 'school1',
                'name': 'School 1',
                'domain': 'school1.localhost',
            },
            {
                'schema': 'school2',
                'name': 'School 2',
                'domain': 'school2.localhost',
            },
        ]

        for tenant_data in demo_tenants:
            schema_name = tenant_data['schema']

            # Skip if already exists
            if Client.objects.filter(schema_name=schema_name).exists():
                self.stdout.write(
                    self.style.WARNING(f'⚠️  Tenant "{tenant_data["name"]}" already exists, skipping...')
                )
                continue

            self.stdout.write(f'\n📦 Creating tenant: {tenant_data["name"]}')

            # Create tenant
            tenant = Client(
                schema_name=schema_name,
                name=tenant_data['name'],
                on_trial=True
            )
            tenant.save()

            # Create domain
            domain = Domain(
                domain=tenant_data['domain'],
                tenant=tenant,
                is_primary=True
            )
            domain.save()

            # Switch to tenant schema to create a demo user
            connection.set_tenant(tenant)

            # Create a demo user for this tenant
            demo_user = User.objects.create_user(
                username='demo',
                email=f'demo@{schema_name}.com',
                password='demo123'
            )

            # Switch back to public schema before next iteration
            connection.set_schema_to_public()

            self.stdout.write(
                self.style.SUCCESS(
                    f'✅ Created tenant "{tenant_data["name"]}"\n'
                    f'   URL: http://{tenant_data["domain"]}:8000\n'
                    f'   Demo user: demo / demo123'
                )
            )

        # Switch back to public schema
        connection.set_schema_to_public()

        self.stdout.write(
            self.style.SUCCESS(
                f'\n\n🎉 Demo setup complete!\n'
                f'\n📝 Demo credentials (same for both tenants):'
                f'\n   Username: demo'
                f'\n   Password: demo123'
                f'\n\n🌐 Access points:'
                f'\n   • Admin Panel: http://localhost:8000/admin/'
                f'\n   • School 1 API: http://school1.localhost:8000/api/'
                f'\n   • School 2 API: http://school2.localhost:8000/api/'
                f'\n\n💡 To get JWT tokens, POST to: http://school1.localhost:8000/api/token/'
                f'\n   with {{"username": "demo", "password": "demo123"}}'
                f'\n\n💡 To create a superuser for admin: python manage.py createsuperuser'
            )
        )
