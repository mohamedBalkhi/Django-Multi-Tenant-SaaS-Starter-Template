#!/bin/bash
# Quick start script for Django Multi-Tenant SaaS

set -e

echo "🚀 Django Multi-Tenant SaaS Quick Start"
echo "========================================"
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "📋 Creating .env file from .env.example..."
    cp .env.example .env
    echo "✅ .env created. Please review and update if needed."
    echo ""
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "🐍 Creating Python virtual environment..."
    python3.12 -m venv venv
    echo "✅ Virtual environment created"
    echo ""
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📦 Installing dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt
echo "✅ Dependencies installed"
echo ""

# Check configuration
echo "🔍 Checking Django configuration..."
python manage.py check
echo "✅ Configuration OK"
echo ""

echo "✨ Setup complete!"
echo ""
echo "📝 Next steps:"
echo ""
echo "1. Start PostgreSQL (if not using Docker):"
echo "   Or use: docker-compose up -d db"
echo ""
echo "2. Run migrations:"
echo "   python manage.py migrate_schemas --shared"
echo "   python manage.py migrate_schemas"
echo ""
echo "3. Create superuser:"
echo "   python manage.py createsuperuser --schema=public"
echo ""
echo "4. Create demo tenants:"
echo "   python manage.py setup_demo"
echo ""
echo "5. Run server:"
echo "   python manage.py runserver"
echo ""
echo "Or use Docker: docker-compose up --build"
