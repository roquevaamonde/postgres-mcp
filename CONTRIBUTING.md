# Contributing to PostgreSQL MCP Server

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing to the project.

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/your-username/postgres-mcp.git
   cd postgres-mcp
   ```

3. **Create a virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   pip install pytest  # For development
   ```

## Development Workflow

### Creating a Feature Branch

```bash
git checkout -b feature/your-feature-name
```

Branch naming conventions:
- `feature/` - New features
- `bugfix/` - Bug fixes
- `docs/` - Documentation updates
- `refactor/` - Code refactoring

### Making Changes

1. Make your changes following the code style guidelines
2. Add tests for new features
3. Run tests to ensure everything works:
   ```bash
   pytest tests/ -v
   ```

4. Commit your changes with clear messages:
   ```bash
   git commit -m "Add feature: description of changes"
   ```

### Code Style Guidelines

- Follow PEP 8 conventions
- Use meaningful variable and function names
- Add type hints to all functions
- Write docstrings for classes and public methods
- Keep functions focused and small (single responsibility)

### Example commit messages

```bash
# Feature
git commit -m "Add support for MySQL connections"

# Bug fix
git commit -m "Fix JSON encoding for datetime objects"

# Documentation
git commit -m "Update CONFIGURATION.md with new options"

# Refactoring
git commit -m "Refactor error handling in DatabaseManager"
```

## Testing

Write tests for all new features and bug fixes.

### Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_postgres_mcp.py -v

# Run specific test
pytest tests/test_postgres_mcp.py::TestDatabaseManager::test_execute_query -v
```

### Test Structure

Tests should follow this pattern:

```python
def test_feature_description(self):
    """Test that the feature does X when Y"""
    # Arrange: Set up test data
    # Act: Perform the action
    # Assert: Verify the result
```

## Documentation

- Update relevant `.md` files in the `docs/` directory
- Keep documentation in sync with code changes
- Use clear, professional language
- Include examples where helpful

## Submitting Changes

### Create a Pull Request

1. **Push your branch**:
   ```bash
   git push origin feature/your-feature-name
   ```

2. **Create Pull Request on GitHub**:
   - Go to the original repository
   - Click "New Pull Request"
   - Select your branch
   - Fill in the PR template

3. **PR Description should include**:
   - What problem does this solve?
   - How does it solve it?
   - Any breaking changes?
   - Related issues (use `#123` to link)

## Code Review Process

1. Maintainers will review your PR
2. Feedback will be provided for any changes needed
3. Once approved, your PR will be merged
4. Your contribution will be included in the next release

## Common Issues

### Tests Failing

```bash
# Clean up __pycache__
find . -type d -name __pycache__ -exec rm -r {} +

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Run tests again
pytest tests/ -v
```

### Import Errors

```bash
# Ensure you're in the venv
source venv/bin/activate

# Reinstall the package in development mode
pip install -e .
```

## Reporting Bugs

Before reporting a bug:

1. Check if it's already reported in Issues
2. Try to reproduce it with the latest code
3. Gather error messages and logs

When reporting, include:
- Python version
- OS and version
- Steps to reproduce
- Expected vs actual behavior
- Error messages/stack traces

## Feature Requests

Before requesting a feature:

1. Check if it's already requested in Issues
2. Explain the use case clearly
3. Provide examples of how you'd use it

## Questions?

- Check the [README.md](README.md) and docs in `docs/`
- Open an Issue with the `question` label
- Review existing Issues for similar questions

## Code of Conduct

- Be respectful and inclusive
- Focus on the code, not the person
- Help others learn and improve
- Report abuse to the maintainers

## License

By contributing, you agree that your contributions will be licensed under the same license as the project (MIT).

---

**Thank you for contributing! Your help makes this project better.** 🙏
