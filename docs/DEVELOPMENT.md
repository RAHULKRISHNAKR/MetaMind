# 🛠️ MetaMind Development Guide

Guide for contributing to MetaMind and setting up your development environment.

---

## 📋 Prerequisites

- **Python 3.11+**
- **Node.js 18+**
- **Git**
- **Docker** (optional, for testing)
- **Groq API Key** (free at [console.groq.com](https://console.groq.com/))

---

## 🚀 Development Setup

### 1. Fork and Clone

```bash
# Fork the repository on GitHub
# Then clone your fork
git clone https://github.com/YOUR_USERNAME/metamind.git
cd metamind

# Add upstream remote
git remote add upstream https://github.com/original/metamind.git
```

### 2. Backend Setup

```bash
# Create virtual environment
cd backend
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install pytest black flake8 mypy

# Configure environment
cp ../.env.example ../.env
# Edit .env and add your GROQ_API_KEY
```

### 3. Frontend Setup

```bash
# Navigate to frontend
cd frontend-react

# Install dependencies
npm install

# Install development tools
npm install -D @types/node @types/react
```

### 4. Run Development Servers

**Terminal 1 - Backend**:
```bash
cd backend
source venv/bin/activate
python run_backend.py
```

**Terminal 2 - Frontend**:
```bash
cd frontend-react
npm run dev
```

---

## 📁 Project Structure

```
MetaMind/
├── backend/
│   ├── agents/              # 11 specialized agents
│   │   ├── __init__.py
│   │   ├── requirement_agent.py
│   │   ├── domain_weight_tuning_agent.py
│   │   ├── architecture_generation_agent.py
│   │   ├── simulation_agent.py
│   │   ├── scoring_engine.py
│   │   ├── optimization_agent.py
│   │   ├── reflection_agent.py
│   │   ├── iteration_agent.py
│   │   ├── versioning_agent.py
│   │   ├── comparison_agent.py
│   │   └── spec_generator_agent.py
│   ├── orchestration/       # LangGraph pipeline
│   │   ├── __init__.py
│   │   ├── graph.py
│   │   └── state.py
│   ├── api/                 # FastAPI endpoints
│   │   ├── __init__.py
│   │   ├── main.py
│   │   └── code_editor_endpoints.py
│   ├── utils/               # Utilities
│   │   ├── __init__.py
│   │   ├── llm_utils.py
│   │   ├── logging_config.py
│   │   └── validation.py
│   └── requirements.txt
├── frontend-react/
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── pages/           # Page components
│   │   ├── services/        # API client
│   │   ├── types/           # TypeScript types
│   │   └── main.tsx
│   └── package.json
├── k8s/                     # Kubernetes manifests
├── docs/                    # Documentation
├── tests/                   # Test files
└── docker-compose.yml
```

---

## 🧪 Testing

### Backend Tests

```bash
cd backend
source venv/bin/activate

# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test file
pytest tests/test_agents.py

# Run specific test
pytest tests/test_agents.py::test_requirement_agent
```

### Frontend Tests

```bash
cd frontend-react

# Run tests
npm test

# Run with coverage
npm test -- --coverage

# Run in watch mode
npm test -- --watch
```

### Integration Tests

```bash
# Start services
docker-compose up -d

# Run integration tests
pytest tests/integration/

# Stop services
docker-compose down
```

---

## 🎨 Code Style

### Python (Backend)

We use **Black** for formatting and **Flake8** for linting.

```bash
# Format code
black backend/

# Check formatting
black --check backend/

# Lint code
flake8 backend/

# Type checking
mypy backend/
```

**Configuration** (`.flake8`):
```ini
[flake8]
max-line-length = 100
exclude = venv,.git,__pycache__
ignore = E203,W503
```

### TypeScript (Frontend)

We use **ESLint** and **Prettier**.

```bash
# Lint code
npm run lint

# Fix linting issues
npm run lint:fix

# Format code
npm run format
```

---

## 🔧 Adding New Features

### Adding a New Agent

1. Create agent file in `backend/agents/`:
```python
# backend/agents/my_new_agent.py
from typing import Dict, Any

class MyNewAgent:
    """Description of what this agent does"""
    
    def process(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process the state and return updated state
        
        Args:
            state: Current pipeline state
            
        Returns:
            Updated state with new information
        """
        # Your logic here
        return state
```

2. Register in orchestration graph (`backend/orchestration/graph.py`):
```python
from backend.agents.my_new_agent import MyNewAgent

# Add to graph
graph.add_node("my_new_agent", MyNewAgent().process)
graph.add_edge("previous_agent", "my_new_agent")
```

3. Add tests (`tests/test_my_new_agent.py`):
```python
import pytest
from backend.agents.my_new_agent import MyNewAgent

def test_my_new_agent():
    agent = MyNewAgent()
    state = {"test": "data"}
    result = agent.process(state)
    assert "expected_key" in result
```

### Adding a New API Endpoint

1. Add endpoint in `backend/api/main.py`:
```python
@app.get("/api/my-endpoint")
async def my_endpoint(param: str):
    """
    Description of endpoint
    
    Args:
        param: Parameter description
        
    Returns:
        Response description
    """
    return {"result": "data"}
```

2. Add request/response models:
```python
from pydantic import BaseModel

class MyRequest(BaseModel):
    field1: str
    field2: int

class MyResponse(BaseModel):
    result: str
```

3. Update API documentation in `docs/API_REFERENCE.md`

### Adding a New Frontend Component

1. Create component file:
```typescript
// frontend-react/src/components/MyComponent.tsx
import React from 'react';

interface MyComponentProps {
  title: string;
  onAction: () => void;
}

export function MyComponent({ title, onAction }: MyComponentProps) {
  return (
    <div>
      <h2>{title}</h2>
      <button onClick={onAction}>Action</button>
    </div>
  );
}
```

2. Add tests:
```typescript
// frontend-react/src/components/MyComponent.test.tsx
import { render, screen, fireEvent } from '@testing-library/react';
import { MyComponent } from './MyComponent';

test('renders component', () => {
  const handleAction = jest.fn();
  render(<MyComponent title="Test" onAction={handleAction} />);
  
  expect(screen.getByText('Test')).toBeInTheDocument();
  
  fireEvent.click(screen.getByText('Action'));
  expect(handleAction).toHaveBeenCalled();
});
```

---

## 🐛 Debugging

### Backend Debugging

**VS Code** (`launch.json`):
```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: FastAPI",
      "type": "python",
      "request": "launch",
      "module": "uvicorn",
      "args": [
        "backend.api.main:app",
        "--reload",
        "--port",
        "8000"
      ],
      "jinja": true,
      "justMyCode": false
    }
  ]
}
```

**Print Debugging**:
```python
import logging
logger = logging.getLogger(__name__)

logger.debug("Debug message")
logger.info("Info message")
logger.error("Error message")
```

### Frontend Debugging

**Browser DevTools**:
- Open Chrome/Firefox DevTools (F12)
- Use React DevTools extension
- Check Network tab for API calls
- Use Console for logging

**VS Code Debugging**:
```json
{
  "type": "chrome",
  "request": "launch",
  "name": "Launch Chrome",
  "url": "http://localhost:5173",
  "webRoot": "${workspaceFolder}/frontend-react/src"
}
```

---

## 📝 Commit Guidelines

We follow **Conventional Commits**:

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types**:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting)
- `refactor`: Code refactoring
- `test`: Adding tests
- `chore`: Maintenance tasks

**Examples**:
```bash
git commit -m "feat(agents): add caching to simulation agent"
git commit -m "fix(api): handle timeout errors in design endpoint"
git commit -m "docs: update API reference with new endpoints"
```

---

## 🔄 Pull Request Process

1. **Create a branch**:
```bash
git checkout -b feature/my-new-feature
```

2. **Make changes and commit**:
```bash
git add .
git commit -m "feat: add my new feature"
```

3. **Push to your fork**:
```bash
git push origin feature/my-new-feature
```

4. **Create Pull Request** on GitHub:
   - Clear title and description
   - Reference related issues
   - Add screenshots if UI changes
   - Ensure CI passes

5. **Code Review**:
   - Address reviewer comments
   - Update PR as needed
   - Squash commits if requested

6. **Merge**:
   - Maintainer will merge when approved
   - Delete branch after merge

---

## 🏗️ Architecture Decisions

### Why LangGraph?
- State management for multi-agent systems
- Conditional routing between agents
- Built-in retry and error handling
- Easy to visualize and debug

### Why FastAPI?
- Automatic API documentation
- Type validation with Pydantic
- Async support for better performance
- Modern Python features

### Why React + Vite?
- Fast development with HMR
- Modern build tooling
- TypeScript support
- Component-based architecture

### Why SQLite?
- Simple setup for development
- No external dependencies
- Easy to backup and migrate
- Can upgrade to PostgreSQL for production

---

## 📚 Resources

### Learning Resources
- [LangChain Documentation](https://python.langchain.com/)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)

### Tools
- [Postman](https://www.postman.com/) - API testing
- [React DevTools](https://react.dev/learn/react-developer-tools) - React debugging
- [DB Browser for SQLite](https://sqlitebrowser.org/) - Database viewer

---

## 🤝 Getting Help

- **GitHub Issues**: Report bugs or request features
- **GitHub Discussions**: Ask questions and share ideas
- **Documentation**: Check docs/ folder
- **Code Comments**: Read inline documentation

---

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Happy coding!** 🚀