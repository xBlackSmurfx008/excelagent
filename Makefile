# Excel Agent - Makefile for Build Automation

.PHONY: help install install-dev test test-cov lint format clean build run dev docker-build docker-run docs

# Default target
help:
	@echo "Excel Agent - Available Commands:"
	@echo "  install      Install production dependencies"
	@echo "  install-dev  Install development dependencies"
	@echo "  test         Run tests"
	@echo "  test-cov     Run tests with coverage"
	@echo "  lint         Run linting checks"
	@echo "  format       Format code with black and isort"
	@echo "  clean        Clean build artifacts"
	@echo "  build        Build the package"
	@echo "  run          Run the application"
	@echo "  dev          Run in development mode"
	@echo "  docker-build Build Docker image"
	@echo "  docker-run   Run with Docker"
	@echo "  docs         Build documentation"

# Installation
install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements-dev.txt
	pre-commit install

# Testing
test:
	pytest tests/ -v

test-cov:
	pytest tests/ --cov=src/excel_agent --cov-report=html --cov-report=term

# Code Quality
lint:
	flake8 src/ tests/
	mypy src/

format:
	black src/ tests/
	isort src/ tests/

format-check:
	black --check src/ tests/
	isort --check-only src/ tests/

# Cleanup
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	find . -type d -name __pycache__ -delete
	find . -type f -name "*.pyc" -delete

# Build
build: clean
	python -m build

# Run Application
run:
	python -m excel_agent.api.dashboard

dev:
	FLASK_ENV=development FLASK_DEBUG=True python -m excel_agent.api.dashboard

# Docker
docker-build:
	docker build -t excel-agent .

docker-run:
	docker run -p 5000:5000 --env-file .env excel-agent

# Documentation
docs:
	mkdocs serve

docs-build:
	mkdocs build

# Database (if needed)
db-migrate:
	alembic upgrade head

db-revision:
	alembic revision --autogenerate -m "$(MSG)"

# Deployment
deploy-dev:
	@echo "Deploying to development environment..."
	# Add deployment commands here

deploy-prod:
	@echo "Deploying to production environment..."
	# Add production deployment commands here

# Monitoring
health-check:
	python scripts/monitoring/health_check.py

# Backup
backup:
	python scripts/maintenance/backup.py

# Full CI Pipeline
ci: format-check lint test-cov
	@echo "CI pipeline completed successfully"
