# Contributing to PDF API Project

Thank you for your interest in contributing to the PDF API Project! This document provides guidelines and information for contributors.

## 🤝 How to Contribute

### 1. Fork the Repository
- Click the "Fork" button on the repository page
- Clone your fork locally: `git clone <your-fork-url>`

### 2. Set Up Development Environment
```bash
# Create virtual environment
python -m venv pdf_api_env

# Activate virtual environment
pdf_api_env\Scripts\activate  # Windows
source pdf_api_env/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt
```

### 3. Create a Feature Branch
```bash
git checkout -b feature/your-feature-name
```

### 4. Make Your Changes
- Follow the existing code style
- Add tests for new features
- Update documentation as needed

### 5. Test Your Changes
```bash
python tests/test_upload.py
python tests/test_llm.py
```

### 6. Submit a Pull Request
- Push your changes to your fork
- Create a pull request with a clear description
- Reference any related issues

## 📝 Code Standards

### Python Code Style
- Follow PEP 8 guidelines
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions focused and small

### Frontend Code
- Use consistent indentation (2 spaces)
- Add comments for complex logic
- Follow semantic HTML principles

### Database Changes
- Always provide migration scripts
- Test database changes thoroughly
- Consider backwards compatibility

## 🧪 Testing

### Running Tests
```bash
# Run all tests
python -m pytest tests/

# Run specific test file
python tests/test_upload.py
```

### Writing Tests
- Write tests for new features
- Ensure good test coverage
- Use descriptive test names

## 📚 Documentation

### Code Documentation
- Add docstrings to all functions
- Update README.md for major changes
- Include examples in documentation

### API Documentation
- Document new endpoints
- Include request/response examples
- Update API version if needed

## 🐛 Bug Reports

When reporting bugs, please include:
- Clear description of the issue
- Steps to reproduce
- Expected vs actual behavior
- Environment details (OS, Python version)
- Relevant error messages

## 💡 Feature Requests

For feature requests, please provide:
- Clear description of the feature
- Use case and benefits
- Possible implementation approach
- Any related issues or PRs

## 🔍 Code Review Process

### What We Look For
- Code quality and readability
- Test coverage
- Documentation updates
- Security considerations
- Performance impact

### Review Timeline
- We aim to review PRs within 48 hours
- Large changes may take longer
- Please be patient and responsive to feedback

## 🚀 Release Process

### Version Numbering
We follow semantic versioning (SemVer):
- MAJOR.MINOR.PATCH
- Major: Breaking changes
- Minor: New features
- Patch: Bug fixes

### Release Notes
- Changelog is maintained in CHANGELOG.md
- Include all significant changes
- Credit contributors

## 📞 Getting Help

### Communication Channels
- GitHub Issues for bugs and features
- GitHub Discussions for questions
- Email maintainers for security issues

### Response Times
- Bug reports: Within 24 hours
- Feature requests: Within 48 hours
- Security issues: Within 2 hours

## 🎉 Recognition

Contributors will be:
- Listed in the README.md
- Mentioned in release notes
- Invited to join the contributors team

## 📋 Checklist for Contributors

Before submitting a PR, ensure:
- [ ] Code follows style guidelines
- [ ] Tests are added and passing
- [ ] Documentation is updated
- [ ] Commit messages are clear
- [ ] No merge conflicts exist

Thank you for contributing to the PDF API Project! 🚀
