# Contributing to Real-Time ML Model Serving API

Thank you for your interest in contributing to this project! 🎉

## 🚀 Getting Started

### Prerequisites

- Go 1.21+
- Python 3.8+
- Redis 7.0+
- Docker & Docker Compose (optional)
- Git

### Development Setup

1. **Fork and clone the repository**

```bash
git clone https://github.com/YOUR_USERNAME/realtime-ml-serving-api.git
cd realtime-ml-serving-api
```

2. **Install Go dependencies**

```bash
cd server
go mod download
```

3. **Install Python dependencies**

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt  # Development dependencies
```

4. **Start Redis for development**

```bash
docker run -d -p 6379:6379 redis:latest
```

5. **Run tests**

```bash
# Go tests
cd server
go test -v ./...

# Python tests
cd ../client
pytest -v
```

## 📝 Code Standards

### Go Code

- Follow [Effective Go](https://golang.org/doc/effective_go) guidelines
- Use `golangci-lint` for linting
- Format code with `gofmt`
- Write table-driven tests
- Minimum 80% test coverage for new code

```bash
# Run linter
golangci-lint run

# Format code
gofmt -w .

# Run tests with coverage
go test -race -coverprofile=coverage.out ./...
go tool cover -html=coverage.out
```

### Python Code

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide
- Use type hints for function signatures
- Write docstrings in NumPy/Google style
- Format code with `black` and `isort`
- Use `flake8` for linting

```bash
# Format code
black client/
isort client/

# Lint
flake8 client/

# Type checking
mypy client/
```

## 🔀 Workflow

### 1. Create a Feature Branch

```bash
git checkout -b feature/amazing-feature
```

Use descriptive branch names:
- `feature/` - New features
- `bugfix/` - Bug fixes
- `docs/` - Documentation updates
- `refactor/` - Code refactoring
- `test/` - Test improvements

### 2. Make Your Changes

- Write clean, readable code
- Add tests for new functionality
- Update documentation
- Keep commits atomic and focused

### 3. Commit Your Changes

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```bash
git commit -m "feat: add model hot-reloading support"
git commit -m "fix: resolve Redis connection timeout"
git commit -m "docs: update API documentation"
```

### 4. Push and Create Pull Request

```bash
git push origin feature/amazing-feature
```

Then open a Pull Request on GitHub.

## ✅ Pull Request Guidelines

### Before Submitting

- [ ] Code follows project style guidelines
- [ ] All tests pass locally
- [ ] New tests added for new features
- [ ] Documentation updated
- [ ] No merge conflicts
- [ ] Commit messages are clear and descriptive

### PR Description Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
How was this tested?

## Checklist
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] All tests passing
- [ ] Code reviewed by myself
```

## 🧪 Testing

### Unit Tests

```bash
# Go
cd server
go test ./... -v

# Python
pytest client/ -v
```

### Integration Tests

```bash
cd tests
go test -v -tags=integration ./...
```

### Load Tests

```bash
cd tests
go test -v -run TestHighLoadStress
```

## 📚 Documentation

- Update README.md for significant changes
- Add inline comments for complex logic
- Update API documentation
- Include examples for new features

## 🐛 Bug Reports

### Good Bug Report Includes

1. **Clear title** - Descriptive summary
2. **Environment** - OS, Go/Python version, Redis version
3. **Steps to reproduce** - Exact steps to reproduce the issue
4. **Expected behavior** - What should happen
5. **Actual behavior** - What actually happens
6. **Logs/Screenshots** - Any relevant output

### Example Bug Report

```markdown
**Title:** Server crashes on invalid model name

**Environment:**
- OS: Ubuntu 22.04
- Go: 1.21.0
- Redis: 7.0.12

**Steps to Reproduce:**
1. Start server with `./ml-server`
2. Send POST to `/predict` with model_name: "nonexistent"
3. Server crashes

**Expected:** 404 error returned
**Actual:** Server panic

**Logs:**
```
panic: runtime error: invalid memory address
```
```

## 💡 Feature Requests

### Good Feature Request Includes

1. **Problem statement** - What problem does this solve?
2. **Proposed solution** - How should it work?
3. **Alternatives considered** - Other approaches?
4. **Additional context** - Examples, mockups, etc.

## 🏷️ Issue Labels

- `bug` - Something isn't working
- `enhancement` - New feature or request
- `documentation` - Documentation improvements
- `good first issue` - Good for newcomers
- `help wanted` - Extra attention needed
- `performance` - Performance improvements
- `security` - Security-related

## 🔍 Code Review Process

1. **Automated checks** - CI/CD pipeline runs tests and linters
2. **Peer review** - At least one maintainer reviews code
3. **Feedback** - Address review comments
4. **Approval** - Maintainer approves PR
5. **Merge** - PR merged to main branch

## 📋 Development Guidelines

### Adding New Features

1. Discuss in GitHub issue first
2. Design API if needed
3. Implement with tests
4. Update documentation
5. Submit PR

### Adding New Models

1. Train model with appropriate framework
2. Save to `models/` directory
3. Add metadata to `config/models.yaml`
4. Update documentation with example

### Performance Improvements

1. Benchmark before changes
2. Make optimization
3. Benchmark after changes
4. Document performance gains
5. Include benchmark results in PR

## 🙏 Recognition

Contributors will be:
- Listed in project credits
- Mentioned in release notes
- Acknowledged in documentation

## 📞 Getting Help

- Open an issue for bugs or features
- Ask questions in GitHub Discussions
- Check existing issues and documentation first

## 📜 Code of Conduct

- Be respectful and inclusive
- Welcome newcomers
- Focus on constructive feedback
- Maintain professional communication

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing! 🚀
