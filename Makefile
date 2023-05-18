# Makefile for Python Project

# Set the default shell to use for executing commands
SHELL := /bin/bash

# Define Python executable
PYTHON := python3

# Define project-specific variables
PROJECT_NAME := serasa_orders
VENV_DIR := venv

# Virtual environment
venv:
	virtualenv venv -p $(PYTHON)
	source $(VENV_DIR)/bin/activate && \
	pip install --upgrade pip && \
	pip install -r requirements.txt

# Linting
lint: venv
	isort .
	flake8 apps

# Testing
test:
	docker compose exec web python manage.py test 

# Build the applications
build:
	docker compose build

# Run the applications
run: build
	docker compose up -d

# Run the postgres application
run-postgres:
	docker compose up db -d

# Run the redis application
run-redis:
	docker compose up redis -d	

# Clean up
clean:
	rm -rf $(VENV_DIR)
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete

security: venv
	safety check

.PHONY: venv format lint test run clean