# Contributing to ClipShot

Thank you for your interest in contributing to ClipShot! This document provides guidelines and instructions for contributing.

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on what is best for the community
- Show empathy towards other community members

## How to Contribute

### Reporting Bugs

Before creating bug reports, please check existing issues. When creating a bug report, include:

- **Clear title and description**
- **Steps to reproduce**
- **Expected behavior**
- **Actual behavior**
- **Screenshots** (if applicable)
- **Environment details** (OS, Node version, Python version, etc.)

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, include:

- **Clear title and description**
- **Use case** - why is this enhancement needed?
- **Proposed solution**
- **Alternatives considered**
- **Additional context**

### Pull Requests

1. **Fork the repository**
2. **Create a branch** from `develop`
   ```bash
   git checkout -b feature/my-feature develop
   ```
3. **Make your changes**
4. **Follow code style guidelines**
5. **Write or update tests**
6. **Update documentation**
7. **Commit your changes**
   ```bash
   git commit -m "feat: add amazing feature"
   ```
8. **Push to your fork**
   ```bash
   git push origin feature/my-feature
   ```
9. **Open a Pull Request**

## Development Workflow

### Branch Naming

- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation changes
- `refactor/` - Code refactoring
- `test/` - Test additions or changes
- `chore/` - Maintenance tasks

### Commit Messages

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <subject>

<body>

<footer>
```

Types:
- `feat` - New feature
- `fix` - Bug fix
- `docs` - Documentation
- `style` - Formatting, missing semicolons, etc.
- `refactor` - Code restructuring
- `test` - Adding tests
- `chore` - Maintenance

Examples:
```
feat(capture): add hardware acceleration support
fix(ui): resolve clip thumbnail loading issue
docs(api): update endpoint documentation
```

## Code Style Guidelines

### Python

- Follow [PEP 8](https://pep8.org/)
- Use type hints
- Maximum line length: 100 characters
- Use docstrings for all public functions/classes

```python
def process_clip(
    clip_id: str,
    options: Dict[str, Any]
) -> ProcessedClip:
    """
    Process a video clip with specified options.
    
    Args:
        clip_id: Unique identifier for the clip
        options: Processing options dictionary
        
    Returns:
        ProcessedClip object with results
        
    Raises:
        ClipNotFoundError: If clip doesn't exist
    """
    pass
```

### TypeScript/React

- Use TypeScript for all new code
- Follow [Airbnb style guide](https://github.com/airbnb/javascript)
- Use functional components and hooks
- Prefer named exports

```typescript
interface ClipCardProps {
  clip: Clip;
  onSelect?: (clip: Clip) => void;
}

export const ClipCard: React.FC<ClipCardProps> = ({ clip, onSelect }) => {
  // Component implementation
};
```

### Rust

- Follow [Rust style guide](https://doc.rust-lang.org/style-guide/)
- Use `cargo fmt` before committing
- Use `cargo clippy` to catch common mistakes

## Testing

### Backend Tests

```bash
cd apps/backend
pytest
```

### Frontend Tests

```bash
cd apps/desktop
npm test
```

### Writing Tests

- Write tests for all new features
- Maintain or improve code coverage
- Test edge cases and error conditions

Example:
```python
def test_clip_processing():
    """Test that clip processing works correctly."""
    clip = create_test_clip()
    result = process_clip(clip.id, {"quality": "high"})
    assert result.status == "success"
    assert result.output_path.exists()
```

## Documentation

- Update README.md if needed
- Add JSDoc/docstrings to new functions
- Update API documentation
- Add examples for new features

## Review Process

1. **Automated checks** must pass (CI/CD)
2. **Code review** by at least one maintainer
3. **Testing** on multiple platforms (if applicable)
4. **Documentation** review
5. **Merge** to develop branch

## Performance Guidelines

- Avoid blocking operations in the main thread
- Use async/await appropriately
- Optimize database queries
- Profile performance-critical code
- Consider memory usage for large operations

## Security Guidelines

- Never commit secrets or API keys
- Validate all user inputs
- Use parameterized queries for database
- Follow OWASP guidelines
- Report security issues privately

## Getting Help

- Join our [Discord](https://discord.gg/clipshot)
- Read the [documentation](../README.md)
- Ask questions in [Discussions](https://github.com/ubeydtalha/Clibshot/discussions)
- Check [existing issues](https://github.com/ubeydtalha/Clibshot/issues)

## Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Given credit in the application (for significant contributions)

Thank you for contributing to ClipShot! 🎉
