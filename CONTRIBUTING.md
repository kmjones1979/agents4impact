# Contributing to Google ADK A2A Multi-Agent System

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing to this project.

## 🚀 Getting Started

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/your-username/google-adk-a2a-agents.git
   cd google-adk-a2a-agents
   ```
3. Set up the development environment:
   ```bash
   make setup
   source venv/bin/activate
   ```

## 💻 Development Workflow

### Creating a New Agent

1. Create a new file in the `agents/` directory
2. Inherit from `BaseAgent` class
3. Implement required methods:
   - `get_tools()` - Define agent capabilities
   - `execute_tool()` - Implement tool execution logic
4. Add the agent to `agents/__init__.py`
5. Update `a2a_server.py` to include the new agent
6. Add tests in `tests/test_agents.py`

Example:

```python
from typing import Any, Dict, List
from .base_agent import BaseAgent

class MyNewAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="My New Agent",
            description="Description of what this agent does",
            instructions="Detailed instructions for agent behavior",
        )

    def get_tools(self) -> List[Dict[str, Any]]:
        return [
            {
                "name": "my_tool",
                "description": "What this tool does",
                "parameters": {...},
            }
        ]

    async def execute_tool(self, tool_name: str, parameters: Dict[str, Any]) -> Any:
        if tool_name == "my_tool":
            return self._my_tool_implementation(parameters)
        return {"error": f"Unknown tool: {tool_name}"}
```

### Code Style

We use:
- **Black** for code formatting
- **Ruff** for linting
- **Type hints** for better code clarity

Format your code before committing:

```bash
black .
ruff check .
```

### Testing

Write tests for all new functionality:

```bash
# Run all tests
make test

# Run specific test file
pytest tests/test_agents.py -v

# Run specific test
pytest tests/test_agents.py::TestMyAgent::test_something -v
```

### Commit Messages

Use clear, descriptive commit messages:

```
feat: Add sentiment analysis agent
fix: Fix BigQuery connection timeout
docs: Update README with deployment guide
test: Add tests for Maps agent geocoding
refactor: Simplify orchestrator routing logic
```

## 📋 Pull Request Process

1. Create a feature branch:
   ```bash
   git checkout -b feature/my-new-feature
   ```

2. Make your changes and commit:
   ```bash
   git add .
   git commit -m "feat: Add my new feature"
   ```

3. Push to your fork:
   ```bash
   git push origin feature/my-new-feature
   ```

4. Open a Pull Request with:
   - Clear description of changes
   - Link to any related issues
   - Screenshots (if applicable)
   - Test results

5. Address review feedback

6. Once approved, your PR will be merged!

## 🐛 Bug Reports

When reporting bugs, include:

- Description of the bug
- Steps to reproduce
- Expected behavior
- Actual behavior
- Environment details (OS, Python version, etc.)
- Error messages or logs

## 💡 Feature Requests

For new features:

- Describe the feature and its use case
- Explain why it would be valuable
- Provide examples if possible
- Consider implementation details

## 🔍 Code Review Guidelines

When reviewing code:

- Be respectful and constructive
- Focus on the code, not the person
- Ask questions to understand the approach
- Suggest improvements with examples
- Approve when satisfied

## 📝 Documentation

- Update README.md for user-facing changes
- Add docstrings to all functions and classes
- Include type hints
- Add inline comments for complex logic
- Update API documentation

## 🎯 Areas for Contribution

We welcome contributions in:

### New Agents
- Cloud Storage agent
- Vertex AI agent  
- Translation agent
- Vision/Image analysis agent
- Cloud Functions deployment agent

### Enhancements
- Add authentication/authorization
- Improve error handling
- Add observability (metrics, tracing)
- Performance optimizations
- Better logging

### Documentation
- More usage examples
- Deployment guides
- Architecture diagrams
- Video tutorials
- Best practices

### Testing
- Unit tests
- Integration tests
- End-to-end tests
- Performance tests
- Load tests

### DevOps
- CI/CD pipelines
- Kubernetes manifests
- Terraform configurations
- Monitoring dashboards

## 🤝 Code of Conduct

- Be respectful and inclusive
- Welcome newcomers
- Accept constructive criticism
- Focus on what's best for the community
- Show empathy towards others

## ❓ Questions?

Feel free to:
- Open an issue for discussion
- Ask in pull request comments
- Reach out to maintainers

Thank you for contributing! 🎉


