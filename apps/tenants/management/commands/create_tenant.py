"""
Management command to create a new tenant
Usage: python manage.py create_tenant --schema=school1 --name="School 1" --domain=school1.localhost --admin-username=admin --admin-email=admin@school1.com
"""
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model
from django.db import connection
from apps.tenants.models import Client, Domain
import getpass

User = get_user_model()


class Command(BaseCommand):
    help = 'Create a new tenant with domain (schema and migrations are created automatically)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--schema',
            type=str,
            required=True,
            help='Schema name (e.g., school1, tenant1)'
        )
        parser.add_argument(
            '--name',
            type=str,
            required=True,
            help='Tenant display name (e.g., "School 1")'
        )
        parser.add_argument(
            '--domain',
            type=str,
            required=True,
            help='Domain name (e.g., school1.localhost or school1.yourdomain.com)'
        )
        parser.add_argument(
            '--paid-until',
            type=str,
            help='Subscription end date (YYYY-MM-DD)'
        )
        parser.add_argument(
            '--on-trial',
            action='store_true',
            default=True,
            help='Set tenant as on trial (default: True)'
        )
        parser.add_argument(
            '--admin-username',
            type=str,
            help='Create initial admin user with this username'
        )
        parser.add_argument(
            '--admin-email',
            type=str,
            help='Email for the initial admin user'
        )
        parser.add_argument(
            '--admin-password',
            type=str,
            help='Password for initial admin user (will prompt if not provided)'
        )

    def handle(self, *args, **options):
        schema_name = options['schema']
        name = options['name']
        domain_name = options['domain']

        # Check if tenant already exists
        if Client.objects.filter(schema_name=schema_name).exists():
            raise CommandError(f'Tenant with schema "{schema_name}" already exists')

        if Domain.objects.filter(domain=domain_name).exists():
            raise CommandError(f'Domain "{domain_name}" already exists')

        self.stdout.write(self.style.MIGRATE_HEADING('Creating tenant...'))
        self.stdout.write(f'  Schema: {schema_name}')
        self.stdout.write(f'  Name: {name}')
        self.stdout.write(f'  Domain: {domain_name}')

        # Create tenant
        tenant = Client(
            schema_name=schema_name,
            name=name,
            on_trial=options.get('on_trial', True)
        )

        if options.get('paid_until'):
            from datetime import datetime
            tenant.paid_until = datetime.strptime(options['paid_until'], '%Y-%m-%d').date()

        # Save tenant - this automatically creates the schema and runs migrations!
        self.stdout.write(self.style.MIGRATE_LABEL('\nCreating PostgreSQL schema and running migrations...'))
        tenant.save()

        # Create domain
        domain = Domain(
            domain=domain_name,
            tenant=tenant,
            is_primary=True
        )
        domain.save()

        # Create initial admin user if requested
        admin_username = options.get('admin_username')
        admin_email = options.get('admin_email')
        admin_password = options.get('admin_password')

        user_created = False
        if admin_username or admin_email:
            self.stdout.write(self.style.MIGRATE_LABEL('\nCreating initial admin user...'))

            # Set defaults
            if not admin_username:
                admin_username = 'admin'
            if not admin_email:
                admin_email = f'admin@{schema_name}.com'

            # Prompt for password if not provided
            if not admin_password:
                admin_password = getpass.getpass('Enter password for admin user: ')
                password_confirm = getpass.getpass('Confirm password: ')

                if admin_password != password_confirm:
                    self.stdout.write(self.style.ERROR('Passwords do not match. User not created.'))
                else:
                    user_created = True
            else:
                user_created = True

            if user_created:
                # Switch to tenant schema to create user
                connection.set_tenant(tenant)

                try:
                    user = User.objects.create_user(
                        username=admin_username,
                        email=admin_email,
                        password=admin_password
                    )
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'✅ Admin user created:\n'
                            f'   Username: {admin_username}\n'
                            f'   Email: {admin_email}'
                        )
                    )
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Error creating user: {e}'))
                    user_created = False
                finally:
                    # Switch back to public schema
                    connection.set_schema_to_public()

        self.stdout.write(
            self.style.SUCCESS(
                f'\n✅ Tenant "{name}" created successfully!\n'
                f'   Schema: {schema_name}\n'
                f'   Domain: {domain_name}\n'
                f'   Status: {"On Trial" if tenant.on_trial else "Active"}\n'
                + (f'   Admin User: {admin_username}\n' if user_created else '') +
                f'\n💡 You can now access this tenant at: http://{domain_name}:8000'
                + (f'\n💡 Login with username "{admin_username}"' if user_created else
                   f'\n💡 Create a user for this tenant: python manage.py shell (see README)')
            )
        )
