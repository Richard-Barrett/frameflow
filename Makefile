# Makefile for FrameFlow

# Variables
PROJECT_NAME=frameflow
PYPI_REPO=pypi

# Default target
.PHONY: help
help:
	@echo "FrameFlow Makefile Commands:"
	@echo "  make install         Install FrameFlow locally in editable mode"
	@echo "  make reinstall       Reinstall FrameFlow (uninstall + editable install)"
	@echo "  make build           Build distribution packages"
	@echo "  make publish         Publish package to PyPI"
	@echo "  make test            Run unit tests with pytest"
	@echo "  make lint            Run pylint for static code analysis"
	@echo "  make format          Format code with black"
	@echo "  make docker-build    Build the FrameFlow Docker image"
	@echo "  make docker-run      Run FrameFlow container with --help"

.PHONY: install
install:
	pip install -e .

.PHONY: reinstall
reinstall:
	pip uninstall -y $(PROJECT_NAME) || true
	pip install -e .

.PHONY: build
build:
	python -m build

.PHONY: publish
publish:
	twine upload --repository $(PYPI_REPO) dist/*

.PHONY: test
test:
	pip install -e .
	@echo "🧪 Running unit tests with pytest..."
	pytest -v --maxfail=1 --disable-warnings tests/

.PHONY: lint
lint:
	@echo "🔍 Running pylint on $(PROJECT_NAME) package..."
	pylint $(PROJECT_NAME)

.PHONY: format
format:
	@echo "🖤 Formatting code with black..."
	black $(PROJECT_NAME) tests

.PHONY: docker-build
docker-build:
	docker build -t $(PROJECT_NAME) .

.PHONY: docker-run
docker-run:
	docker run --rm $(PROJECT_NAME) --help
