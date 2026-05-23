# Contributing to AI Agents Platform

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing to the project.

## Code of Conduct

Be respectful, inclusive, and professional in all interactions.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/TestGitHub.git`
3. Add upstream: `git remote add upstream https://github.com/Grachik2007/TestGitHub.git`
4. Create a branch: `git checkout -b feature/your-feature`

## Development Setup

See [DEPLOYMENT.md](./DEPLOYMENT.md) for setup instructions.

## Code Style

### Python (Backend)
```bash
# Format with Black
black apps/api/

# Sort imports with isort
isort apps/api/

# Lint with Flake8
flake8 apps/api/

# Type check with Mypy
mypy apps/api/
```

### JavaScript/TypeScript (Frontend)
```bash
# Format with Prettier
npm run format --prefix apps/web

# Lint with ESLint
npm run lint --prefix apps/web

# Type check
npm run type-check --prefix apps/web
```

## Commit Messages

Follow conventional commits:

```
<type>[optional scope]: <description>

[optional body]

[optional footer]
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Code style
- `refactor`: Refactoring
- `test`: Tests
- `chore`: Build, CI, dependencies

Example:
```
feat(agents): add support for custom agent prompts

This allows users to customize agent behavior with custom prompts.

Closes #123
```

## Pull Request Process

1. Update documentation as needed
2. Add tests for new functionality
3. Ensure all tests pass: `pytest` (backend) and `npm test` (frontend)
4. Follow code style guidelines
5. Create a descriptive pull request

## Testing

### Backend Tests
```bash
cd apps/api
pytest                  # Run all tests
pytest --cov=.         # With coverage
pytest tests/test_*.py # Run specific tests
```

### Frontend Tests
```bash
cd apps/web
npm test                # Run tests
npm test -- --coverage # With coverage
```

## Documentation

- Update README.md for user-facing changes
- Add docstrings to Python functions
- Add JSDoc comments to JavaScript functions
- Update ARCHITECTURE.md for architectural changes

## Reporting Issues

Use GitHub Issues with:
- Clear, descriptive title
- Detailed description
- Steps to reproduce
- Expected vs actual behavior
- Screenshots (if applicable)
- Environment information

## Feature Requests

Use GitHub Issues to suggest new features with:
- Clear problem statement
- Proposed solution
- Alternative approaches
- Use cases

## Performance

When optimizing:
1. Measure before and after
2. Document the change
3. Consider trade-offs
4. Update benchmarks if applicable

## Security

For security vulnerabilities:
1. **Do NOT** create a public issue
2. Email security details privately
3. Allow time for a patch before disclosure
4. Follow responsible disclosure

## Questions?

- Check existing issues/discussions
- Review documentation
- Ask in discussions tab
- Create a new issue with [QUESTION] label

## License

By contributing, you agree your code will be licensed under the MIT License.

---

Thank you for contributing to making AI Agents Platform better! 🎉
