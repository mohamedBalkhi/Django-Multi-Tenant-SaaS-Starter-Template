.PHONY: help setup migrate run test clean docker-up docker-down demo

help:
	@echo "Django Multi-Tenant SaaS - Available Commands"
	@echo "=============================================="
	@echo "make setup        - Initial project setup"
	@echo "make migrate      - Run database migrations for all tenants"
	@echo "make run          - Run development server"
	@echo "make test         - Run test suite"
	@echo "make test-cov     - Run tests with coverage report"
	@echo "make clean        - Clean Python cache files"
	@echo "make docker-up    - Start Docker containers"
	@echo "make docker-down  - Stop Docker containers"
	@echo "make demo         - Create demo tenants"
	@echo "make shell        - Open Django shell"
	@echo "make superuser    - Create superuser for admin"

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
	@echo "Starting development server..."
	. venv/bin/activate && python manage.py runserver

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
	@echo "Starting Docker containers..."
	docker-compose up --build

docker-down:
	@echo "Stopping Docker containers..."
	docker-compose down

demo:
	@echo "Creating demo tenants..."
	. venv/bin/activate && python manage.py setup_demo

shell:
	@echo "Opening Django shell..."
	. venv/bin/activate && python manage.py shell

superuser:
	@echo "Creating superuser for admin panel..."
	. venv/bin/activate && python manage.py createsuperuser --schema=public
