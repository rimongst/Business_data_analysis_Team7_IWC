# Variables
VENV ?= venv
PYTHON = $(VENV)/bin/python

# Install dependencies
install:
	@echo "📦 Installing dependencies..."
	pip install --upgrade pip
	pip install -r requirements/base.txt
	pip install -r requirements/dev.txt
	@echo "✅ Installation complete."

update_exchange_rate:
	@echo "🔄 Fetching latest exchange rates..."
	python src/data_ingestion/upload_new_exchange_rate.py
	@echo "✅ Exchange rates updated."

# Run the pipeline
run:
	@echo "🚀 Running BDA pipeline..."
	python src/main.py

# Format code (Black + isort)
format:
	@echo "🛠 Formatting code..."
	black src/
	isort src/
	@echo "✅ Formatting complete."

# Lint code (flake8)
lint:
	@echo "🔍 Running lint checks..."
	flake8 src/
	@echo "✅ Linting complete."

# Run tests
test:
	@echo "🧪 Running tests..."
	pytest tests/
	@echo "✅ Tests complete."

# Clean up temporary files
clean:
	@echo "🧹 Cleaning up temporary files..."
	find . -name '*.pyc' -delete
	find . -name '__pycache__' -delete
	@echo "✅ Cleanup complete."

# Set up pre-commit hooks
precommit:
	@echo "⚙️ Setting up pre-commit hooks..."
	pre-commit install
	@echo "✅ Pre-commit installed."
