.PHONY: help setup migrate run test clean docker-up docker-down docker-logs docker-rebuild demo shell shell-plus

help:
	@echo "Django Multi-Tenant SaaS - Available Commands"
	@echo "=============================================="
	@echo ""
	@echo "🚀 Development (Docker):"
	@echo "  make docker-up       - Start Docker containers (with auto-reload)"
	@echo "  make docker-down     - Stop Docker containers"
	@echo "  make docker-logs     - View logs (follow mode)"
	@echo "  make docker-rebuild  - Rebuild and restart containers"
	@echo "  make docker-shell    - Access Django shell in container"
	@echo ""
	@echo "🛠️  Local Development:"
	@echo "  make setup           - Initial project setup"
	@echo "  make migrate         - Run database migrations for all tenants"
	@echo "  make run             - Run development server (with watchdog)"
	@echo "  make shell           - Open Django shell"
	@echo "  make shell-plus      - Open enhanced Django shell (shell_plus)"
	@echo ""
	@echo "🧪 Testing:"
	@echo "  make test            - Run test suite"
	@echo "  make test-cov        - Run tests with coverage report"
	@echo ""
	@echo "🗄️  Database:"
	@echo "  make demo            - Create demo tenants"
	@echo "  make superuser       - Create superuser for admin"
	@echo ""
	@echo "🧹 Maintenance:"
	@echo "  make clean           - Clean Python cache files"

setup:
	@echo "Setting up project..."
	cp -n .env.example .env || true
	python3.12 -m venv venv
	. venv/bin/activate && pip install -r requirements.txt
	@echo "✅ Setup complete! Activate venv: source venv/bin/activate"

migrate:
	@echo "Running migrations for all tenants..."
	. venv/bin/activate && python manage.py migrate_schemas

run:
	@echo "Starting development server with auto-reload..."
	. venv/bin/activate && python manage.py runserver_plus

test:
	@echo "Running tests..."
	. venv/bin/activate && POSTGRES_HOST=localhost pytest

test-cov:
	@echo "Running tests with coverage..."
	. venv/bin/activate && POSTGRES_HOST=localhost pytest --cov=apps --cov-report=html --cov-report=term

clean:
	@echo "Cleaning cache files..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	@echo "✅ Cleaned!"

docker-up:
	@echo "🚀 Starting Docker containers with auto-reload..."
	@echo "📝 Files will auto-reload when you save changes!"
	docker-compose up --build

docker-down:
	@echo "Stopping Docker containers..."
	docker-compose down

docker-logs:
	@echo "Following Docker logs (Ctrl+C to exit)..."
	docker-compose logs -f web

docker-rebuild:
	@echo "Rebuilding Docker containers..."
	docker-compose down
	docker-compose build --no-cache
	docker-compose up

docker-shell:
	@echo "Opening Django shell in Docker container..."
	docker-compose exec web python manage.py shell_plus

demo:
	@echo "Creating demo tenants..."
	. venv/bin/activate && python manage.py setup_demo

shell:
	@echo "Opening Django shell..."
	. venv/bin/activate && python manage.py shell

shell-plus:
	@echo "Opening enhanced Django shell with auto-imports..."
	. venv/bin/activate && python manage.py shell_plus

superuser:
	@echo "Creating superuser for admin panel..."
	. venv/bin/activate && python manage.py createsuperuser --schema=public
