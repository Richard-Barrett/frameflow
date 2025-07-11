# Makefile for FrameFlow

# ================================
# ⚙️  Variables
# ================================
PROJECT_NAME=frameflow
PYPI_REPO=pypi
VENV_DIR=venv
PYTHON=$(VENV_DIR)/bin/python
PIP=$(VENV_DIR)/bin/pip

# ================================
# 🆘 Help
# ================================
.PHONY: help
help:
	@echo ""
	@echo "📝 FrameFlow Makefile Commands:"
	@echo ""
	@echo "  make venv           Create Python virtual environment"
	@echo "  make install        Install FrameFlow locally in editable mode"
	@echo "  make reinstall      Reinstall FrameFlow (uninstall + editable install)"
	@echo "  make build          Build distribution packages"
	@echo "  make publish        Publish package to PyPI"
	@echo "  make test           Run unit tests with pytest"
	@echo "  make lint           Run pylint for static code analysis"
	@echo "  make format         Format code with black"
	@echo "  make docker-build   Build the FrameFlow Docker image"
	@echo "  make docker-run     Run FrameFlow container with --help"
	@echo "  make clean          Remove __pycache__ and .pytest_cache"
	@echo ""

# ================================
# 🐍 Virtual Environment
# ================================
.PHONY: venv
venv:
	@if [ ! -d "$(VENV_DIR)" ]; then \
		echo "🔧 Creating venv..."; \
		python3 -m venv $(VENV_DIR); \
		echo "✅ venv created in $(VENV_DIR)."; \
	else \
		echo "✅ venv already exists."; \
	fi
	@echo "💡 To activate, run: source $(VENV_DIR)/bin/activate"

# ================================
# 📦 Installation
# ================================
.PHONY: install
install: venv
	@echo "📦 Installing FrameFlow into venv..."
	$(PIP) install --upgrade pip
	$(PIP) install -e .
	$(PIP) install -r requirements.txt
	@echo "✅ FrameFlow installed. Activate with 'source $(VENV_DIR)/bin/activate'"

.PHONY: reinstall
reinstall: venv
	@echo "🔄 Reinstalling FrameFlow..."
	$(PIP) uninstall -y $(PROJECT_NAME) || true
	$(MAKE) install

# ================================
# 🛠️  Build and Publish
# ================================
.PHONY: build
build:
	@echo "📦 Building distribution packages..."
	$(PYTHON) -m build

.PHONY: publish
publish:
	@echo "🚀 Publishing package to PyPI..."
	twine upload --repository $(PYPI_REPO) dist/*

# ================================
# 🧪 Testing
# ================================
.PHONY: test
test: install
	@echo "🧪 Running unit tests with pytest..."
	$(VENV_DIR)/bin/pytest -v --maxfail=1 --disable-warnings tests/

# ================================
# 🔍 Linting
# ================================
.PHONY: lint
lint: install
	@echo "🔍 Running pylint on $(PROJECT_NAME) package..."
	$(VENV_DIR)/bin/pylint $(PROJECT_NAME)

# ================================
# 🖤 Formatting
# ================================
.PHONY: format
format: install
	@echo "🖤 Formatting code with black..."
	$(VENV_DIR)/bin/black $(PROJECT_NAME) tests

# ================================
# 🐳 Docker
# ================================
.PHONY: docker-build
docker-build:
	@echo "🐳 Building FrameFlow Docker image..."
	docker build -t $(PROJECT_NAME) .

.PHONY: docker-run
docker-run:
	@echo "🐳 Running FrameFlow Docker container..."
	docker run --rm $(PROJECT_NAME) --help

# ================================
# 🧹 Cleaning
# ================================
.PHONY: clean
clean:
	@echo "🧹 Cleaning __pycache__ and .pytest_cache..."
	find . -type d -name "__pycache__" -exec rm -r {} +
	rm -rf .pytest_cache
