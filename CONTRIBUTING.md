# Contributing to MetaMind

Thank you for your interest in contributing to MetaMind! This document provides guidelines and instructions for contributing.

## 🤝 How to Contribute

### Reporting Bugs

If you find a bug, please create an issue with:
- Clear description of the bug
- Steps to reproduce
- Expected vs actual behavior
- Environment details (OS, Python version, etc.)
- Relevant logs or screenshots

### Suggesting Features

Feature requests are welcome! Please create an issue with:
- Clear description of the feature
- Use case and benefits
- Proposed implementation (if applicable)

### Pull Requests

1. **Fork the repository**
   ```bash
   git clone https://github.com/yourusername/metamind.git
   cd metamind
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Follow the existing code style
   - Add tests for new features
   - Update documentation as needed
   - Ensure all tests pass

4. **Commit your changes**
   ```bash
   git add .
   git commit -m "Add: brief description of changes"
   ```

5. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Create a Pull Request**
   - Provide a clear description
   - Reference any related issues
   - Wait for review

## 📝 Code Style

### Python
- Follow PEP 8 guidelines
- Use type hints
- Add docstrings to functions and classes
- Keep functions focused and small

### Example
```python
def calculate_score(metrics: Dict[str, float], weights: Dict[str, float]) -> float:
    """
    Calculate weighted score from metrics.
    
    Args:
        metrics: Dictionary of metric names to values
        weights: Dictionary of metric names to weights
        
    Returns:
        Weighted score as float
    """
    return sum(metrics[k] * weights[k] for k in metrics)
```

## 🧪 Testing

### Running Tests
```bash
# Install test dependencies
pip install pytest pytest-cov

# Run all tests
pytest

# Run with coverage
pytest --cov=backend --cov-report=html
```

### Writing Tests
- Place tests in `tests/` directory
- Name test files `test_*.py`
- Use descriptive test names
- Test edge cases and error conditions

## 📚 Documentation

### Updating Documentation
- Update relevant `.md` files
- Add examples for new features
- Keep documentation clear and concise
- Use proper markdown formatting

### Docstrings
- Use Google-style docstrings
- Include parameter types and descriptions
- Document return values
- Add usage examples for complex functions

## 🏗️ Project Structure

```
MetaMind/
├── backend/
│   ├── agents/          # AI agents
│   ├── api/            # FastAPI endpoints
│   ├── orchestration/  # LangGraph pipeline
│   └── requirements.txt
├── frontend/
│   ├── app.py          # Streamlit app
│   └── requirements.txt
├── tests/              # Test files
├── docs/               # Additional documentation
└── README.md
```

## 🔍 Code Review Process

1. **Automated Checks**
   - Code style (flake8, black)
   - Type checking (mypy)
   - Tests (pytest)
   - Coverage (pytest-cov)

2. **Manual Review**
   - Code quality
   - Documentation
   - Test coverage
   - Performance considerations

3. **Approval**
   - At least one maintainer approval required
   - All checks must pass
   - No unresolved comments

## 🎯 Areas for Contribution

### High Priority
- [ ] Additional architecture templates
- [ ] More domain weight configurations
- [ ] Performance optimizations
- [ ] Test coverage improvements

### Medium Priority
- [ ] Kubernetes deployment manifests
- [ ] PostgreSQL support
- [ ] Redis caching layer
- [ ] Prometheus metrics

### Low Priority
- [ ] Additional LLM providers
- [ ] Custom visualization options
- [ ] Export formats (PDF, DOCX)
- [ ] Multi-language support

## 💬 Communication

- **Issues**: For bugs and feature requests
- **Discussions**: For questions and ideas
- **Pull Requests**: For code contributions

## 📜 License

By contributing, you agree that your contributions will be licensed under the MIT License.

## 🙏 Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes
- Project documentation

Thank you for contributing to MetaMind! 🎉