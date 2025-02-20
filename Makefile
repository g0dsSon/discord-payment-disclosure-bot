# Variables
PYTHON = python
PIP = pip
PYTEST = pytest
BLACK = black
ISORT = isort
FLAKE8 = flake8
CONFIG_DIR = src/bot/config

# Default target
.PHONY: help
help:
	@echo "Available commands:"
	@echo "  install       Install dependencies"
	@echo "  lint          Run linters (black, isort, flake8)"
	@echo "  test          Run tests with pytest"
	@echo "  format        Format code with black and isort"
	@echo "  build         Build the package"
	@echo "  clean         Clean up build artifacts"
	@echo "  run           Run the bot"
	@echo "  config        Create initial config from example"

# Create a python virtual environment
.PHONY: venv
venv:
	$(PYTHON) -m venv .venv

# Install dependencies
.PHONY: install
install:
	$(PIP) install -e ".[dev]"

# Create initial config
.PHONY: config
config:
	@if [ ! -f "$(CONFIG_DIR)/config.toml" ]; then \
		cp "$(CONFIG_DIR)/config.example.toml" "$(CONFIG_DIR)/config.toml"; \
		echo "Created config.toml from example. Please edit with your settings."; \
	else \
		echo "config.toml already exists."; \
	fi

# Run linters
.PHONY: lint
lint:
	$(BLACK) src tests
	$(ISORT) src tests
	$(FLAKE8) src tests

# Run tests
.PHONY: test
test:
	$(PYTEST) --cov=src tests

# Format code
.PHONY: format
format:
	$(BLACK) src tests
	$(ISORT) src tests

# Build the package
.PHONY: build
build:
	$(PYTHON) -m build

# Clean up build artifacts
.PHONY: clean
clean:
	rm -rf  .venv src/*.egg-info
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

# Run the bot
.PHONY: run
run:
	$(PYTHON) -m bot.core

# # Fly.io deployment commands
# .PHONY: fly-launch
# fly-launch:
#     flyctl launch --now

# .PHONY: fly-logs
# fly-logs:
#     flyctl logs

# .PHONY: fly-token
# fly-token:
#     @read -p "Enter Discord Token: " token; \
#     flyctl secrets set DISCORD_TOKEN=$$token
