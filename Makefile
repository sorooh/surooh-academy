# Makefile for Surooh Academy
.PHONY: help install install-dev test test-cov lint format clean run docker-build docker-run

# Default target
help:
	@echo "🚀 Surooh Academy - AI Bot Factory"
	@echo ""
	@echo "Available commands:"
	@echo "  📦 install        Install production dependencies"
	@echo "  🛠️  install-dev     Install development dependencies"
	@echo "  🧪 test           Run tests"
	@echo "  📊 test-cov       Run tests with coverage report"
	@echo "  🔍 lint           Run linting (flake8, black, isort)"
	@echo "  ✨ format         Format code (black, isort)"
	@echo "  🧹 clean          Clean up generated files"
	@echo "  🚀 run            Run the application locally"
	@echo "  🐳 docker-build   Build Docker image"
	@echo "  🐳 docker-run     Run with Docker Compose"
	@echo "  📈 monitor        Start monitoring stack"
	@echo "  🔒 security       Run security checks"

# Installation
install:
	pip install -r requirements.txt

install-dev: install
	pip install -r requirements-test.txt

# Testing
test:
	pytest tests/ -v

test-cov:
	pytest tests/ -v --cov=. --cov-report=html --cov-report=term

test-watch:
	pytest-watch tests/

# Code quality
lint:
	flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
	black --check .
	isort --check-only .
	mypy .

format:
	black .
	isort .

# Security
security:
	bandit -r . -f json -o bandit-report.json
	safety check --json --output safety-report.json

# Development
run:
	uvicorn main:app --reload --host 0.0.0.0 --port 8000

run-prod:
	uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4

# Docker
docker-build:
	docker build -t surooh-academy .

docker-run:
	docker-compose up -d

docker-stop:
	docker-compose down

docker-logs:
	docker-compose logs -f

# Monitoring
monitor:
	docker-compose -f docker-compose.yml up -d prometheus grafana

# Cleanup
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf htmlcov/
	rm -rf .coverage
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf dist/
	rm -rf build/

# Database
db-upgrade:
	alembic upgrade head

db-downgrade:
	alembic downgrade -1

db-revision:
	alembic revision --autogenerate -m "$(message)"

# Deployment
deploy-staging:
	@echo "🚀 Deploying to staging..."
	# Add staging deployment commands here

deploy-prod:
	@echo "🚀 Deploying to production..."
	# Add production deployment commands here

# Backup
backup:
	@echo "💾 Creating backup..."
	# Add backup commands here

# Health checks
health:
	curl -f http://localhost:8000/health || exit 1

ready:
	curl -f http://localhost:8000/ready || exit 1

# Documentation
docs-serve:
	@echo "📚 Serving documentation at http://localhost:8000/docs"
	python -m webbrowser http://localhost:8000/docs

# Environment setup
setup-env:
	cp .env.example .env
	@echo "✅ Environment file created. Please edit .env with your settings."

# Git hooks
install-hooks:
	pre-commit install
	@echo "✅ Pre-commit hooks installed"

# Quick start
quickstart: setup-env install-dev
	@echo "🎉 Quick start complete!"
	@echo "📝 Edit .env file with your configuration"
	@echo "🚀 Run 'make run' to start the application"