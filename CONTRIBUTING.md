# Contributing to VetrAI Platform

Thank you for your interest in contributing to VetrAI! This document provides guidelines and instructions for contributing to the project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Making Changes](#making-changes)
- [Pull Request Process](#pull-request-process)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Documentation](#documentation)

## Code of Conduct

We are committed to providing a welcoming and inclusive environment for all contributors. Please:

- Be respectful and considerate
- Welcome newcomers and help them get started
- Focus on what is best for the community
- Show empathy towards other community members

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/your-username/vetrai_v5.git
   cd vetrai_v5
   ```

3. **Add upstream remote**:
   ```bash
   git remote add upstream https://github.com/bininfotech0/vetrai_v5.git
   ```

4. **Create a branch** for your changes:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Development Setup

### Prerequisites

- Docker & Docker Compose
- Python 3.11+
- Node.js 18+
- PostgreSQL 15+
- Redis 7+

### Local Environment Setup

1. **Copy environment file**:
   ```bash
   cp .env.example .env
   ```

2. **Start services with Docker Compose**:
   ```bash
   docker-compose up -d
   ```

3. **Run database migrations**:
   ```bash
   ./scripts/setup/migrate.sh
   ```

4. **Install Python dependencies** (for local development):
   ```bash
   cd services/auth
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

## Making Changes

### Branch Naming Convention

- `feature/description` - New features
- `bugfix/description` - Bug fixes
- `docs/description` - Documentation changes
- `refactor/description` - Code refactoring
- `test/description` - Test additions or modifications

### Commit Message Format

Follow the conventional commits format:

```
<type>(<scope>): <subject>

<body>

<footer>
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Test changes
- `chore`: Build process or auxiliary tool changes

Example:
```
feat(auth): add password reset functionality

Implement password reset via email with secure token generation.
Tokens expire after 24 hours.

Closes #123
```

## Pull Request Process

1. **Update your branch** with the latest upstream changes:
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. **Ensure all tests pass**:
   ```bash
   pytest
   ```

3. **Update documentation** if needed

4. **Push your changes**:
   ```bash
   git push origin feature/your-feature-name
   ```

5. **Create a Pull Request** on GitHub with:
   - Clear title and description
   - Reference to related issues
   - Screenshots (if UI changes)
   - Test results

6. **Address review feedback** promptly

7. **Squash commits** if requested

## Coding Standards

### Python

- Follow [PEP 8](https://pep8.org/) style guide
- Use type hints where appropriate
- Write docstrings for all functions and classes
- Maximum line length: 100 characters

Example:
```python
def create_user(
    email: str,
    password: str,
    organization_id: int
) -> User:
    """
    Create a new user account.
    
    Args:
        email: User's email address
        password: Plain text password (will be hashed)
        organization_id: ID of the organization
    
    Returns:
        Created User instance
    
    Raises:
        ValueError: If email already exists
    """
    # Implementation
    pass
```

### JavaScript/TypeScript

- Use ES6+ features
- Follow [Airbnb JavaScript Style Guide](https://github.com/airbnb/javascript)
- Use TypeScript for type safety
- Write JSDoc comments

### SQL

- Use uppercase for SQL keywords
- Use snake_case for table and column names
- Add appropriate indexes
- Include comments for complex queries

## Testing

### Backend Testing

```bash
# Run all tests
pytest

# Run specific service tests
pytest services/auth/tests/

# Run with coverage
pytest --cov=services --cov-report=html

# View coverage report
open htmlcov/index.html
```

### Test Structure

```python
import pytest
from fastapi.testclient import TestClient

def test_user_registration():
    """Test user registration endpoint"""
    # Arrange
    user_data = {...}
    
    # Act
    response = client.post("/api/v1/register", json=user_data)
    
    # Assert
    assert response.status_code == 201
    assert response.json()["email"] == user_data["email"]
```

## Documentation

### API Documentation

- Use OpenAPI/Swagger annotations
- Provide examples for all endpoints
- Document all request/response schemas
- Include error responses

### Code Documentation

- Write clear docstrings
- Explain complex logic with comments
- Keep documentation up-to-date with code changes

### Architecture Documentation

Update `/docs/architecture/` when making significant changes:
- System design decisions
- Database schema changes
- New service additions
- Integration patterns

## Security

### Reporting Security Issues

**DO NOT** create public issues for security vulnerabilities. Instead:

1. Email: security@vetrai.io
2. Include:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

### Security Best Practices

- Never commit secrets or credentials
- Use environment variables for configuration
- Validate and sanitize all inputs
- Use parameterized queries
- Implement proper authentication and authorization
- Keep dependencies up-to-date

## Review Process

### What We Look For

- Code quality and style
- Test coverage
- Documentation
- Performance implications
- Security considerations
- Backward compatibility

### Review Timeline

- Initial review: Within 2-3 business days
- Follow-up reviews: Within 1-2 business days
- Minor changes: Potentially same day

## Getting Help

- **Documentation**: Check `/docs` directory
- **Discord**: [Join our community](https://discord.gg/vetrai)
- **Issues**: Search existing issues or create a new one
- **Email**: dev@vetrai.io

## License

By contributing to VetrAI, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to VetrAI! 🚀
