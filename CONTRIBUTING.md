# 🤝 Contributing to Surooh Academy

Thank you for your interest in contributing to Surooh Academy! This document provides guidelines and information for contributors.

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- Docker & Docker Compose
- Google Cloud Account (for testing AI features)
- Git

### Development Setup

1. **Fork and Clone**
   ```bash
   git clone https://github.com/your-username/surooh-academy.git
   cd surooh-academy
   ```

2. **Environment Setup**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

4. **Pre-commit Hooks**
   ```bash
   pre-commit install
   ```

## 🏗️ Development Workflow

### Code Style

- **Formatting**: Black, isort
- **Linting**: flake8, pylint
- **Type Checking**: mypy
- **Documentation**: Google-style docstrings

### Running Tests

```bash
# All tests
pytest

# With coverage
pytest --cov=server --cov-report=html

# Specific test file
pytest tests/test_academy.py
```

### Code Formatting

```bash
# Format code
black .
isort .

# Check formatting
black --check .
isort --check-only .

# Lint
flake8 .
mypy server/
```

## 📝 Contribution Guidelines

### Branch Naming

- `feature/your-feature-name`
- `bugfix/issue-description`
- `docs/documentation-update`
- `refactor/component-name`

### Commit Messages

Use [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: add semantic search endpoint
fix: resolve memory leak in orchestrator
docs: update API documentation
refactor: simplify bot training logic
test: add integration tests for academy
```

### Pull Request Process

1. **Create Feature Branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```

2. **Develop and Test**
   - Write code following our style guide
   - Add/update tests
   - Update documentation

3. **Pre-PR Checklist**
   - [ ] Tests pass locally
   - [ ] Code is formatted (black, isort)
   - [ ] No linting errors
   - [ ] Documentation updated
   - [ ] Commit messages follow convention

4. **Submit PR**
   - Clear title and description
   - Link related issues
   - Add screenshots/videos if UI changes

## 🧪 Testing Guidelines

### Test Structure
```
tests/
├── unit/           # Unit tests
├── integration/    # Integration tests
├── e2e/           # End-to-end tests
├── fixtures/      # Test data
└── conftest.py    # Pytest configuration
```

### Writing Tests

```python
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

@pytest.mark.asyncio
async def test_academy_intake():
    # Test academy intake functionality
    pass
```

## 📚 Documentation

### API Documentation

- Use FastAPI's automatic documentation
- Add comprehensive docstrings
- Include examples in endpoint descriptions

### Code Documentation

```python
def train_bot(bot_config: Dict[str, Any]) -> BotTrainingResult:
    """
    Train a specialized bot with given configuration.
    
    Args:
        bot_config: Configuration dictionary containing:
            - name: Bot name
            - type: Bot type (customer_support, pricing, etc.)
            - capabilities: List of bot capabilities
            
    Returns:
        BotTrainingResult: Training results with metrics and plan
        
    Raises:
        ValidationError: If bot_config is invalid
        TrainingError: If training fails
        
    Example:
        >>> config = {"name": "support_bot", "type": "customer_support"}
        >>> result = train_bot(config)
        >>> print(result.success)
        True
    """
```

## 🌟 Areas for Contribution

### High Priority
- [ ] **Bot Specializations**: Add new bot types
- [ ] **Integrations**: Connect with external services
- [ ] **Performance**: Optimize AI processing
- [ ] **Security**: Enhance authentication/authorization

### Medium Priority
- [ ] **UI/UX**: Improve web interface
- [ ] **Monitoring**: Add more metrics and alerts
- [ ] **Documentation**: Tutorials and guides
- [ ] **Testing**: Increase test coverage

### Good First Issues
- [ ] **Bug Fixes**: Small bug fixes
- [ ] **Documentation**: Fix typos, add examples
- [ ] **Code Quality**: Refactor small functions
- [ ] **Tests**: Add unit tests for utilities

## 🏛️ Architecture Guidelines

### Code Organization
```
server/
├── academy/           # Core academy functionality
│   ├── instructor.py  # Main AI instructor
│   ├── trainers/     # Specialized trainers
│   └── orchestrator.py # Multi-agent coordination
├── core/             # Core utilities
│   ├── memory_*      # Memory and knowledge management
│   └── monitoring/   # System monitoring
└── integrations/     # External service integrations
```

### Design Principles

1. **Modularity**: Each component should be self-contained
2. **Async First**: Use async/await for I/O operations
3. **Type Safety**: Use type hints everywhere
4. **Error Handling**: Graceful error handling with proper logging
5. **Configuration**: Use environment variables for config

## 🚀 Deployment

### Local Development
```bash
# Using Docker Compose
docker-compose up -d

# Direct Python
uvicorn main:app --reload --host 0.0.0.0 --port 5000
```

### Production
- Docker images are built automatically
- Deployed via GitHub Actions
- Monitoring with Prometheus/Grafana

## 🤝 Community Guidelines

### Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Help newcomers get started
- Follow the [GitHub Community Guidelines](https://docs.github.com/en/github/site-policy/github-community-guidelines)

### Getting Help

- 📖 [Documentation](https://docs.surooh-academy.com)
- 💬 [Discord Community](https://discord.gg/surooh)
- 🐛 [GitHub Issues](https://github.com/sorooh/surooh-academy/issues)
- 📧 [Email Support](mailto:support@surooh-academy.com)

## 📄 License

By contributing to Surooh Academy, you agree that your contributions will be licensed under the same license as the project.

---

**Thank you for contributing to Surooh Academy! 🎉**

Your contributions help make AI more accessible and powerful for everyone.