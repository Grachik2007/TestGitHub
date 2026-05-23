# Agents Package

AI Agent implementations and orchestration.

## Agents

1. SEO Agent
2. Supplier Agent
3. Product Agent
4. Pricing Agent

## Structure

```
agents/
├── base.py          # Base agent class
├── dispatcher.py    # Agent routing
├── seo/            # SEO agent
├── supplier/       # Supplier agent
├── product/        # Product agent
└── pricing/        # Pricing agent
```

## Usage

```python
from agents import AgentDispatcher

dispatcher = AgentDispatcher()
result = dispatcher.execute("seo", prompt="Analyze keywords")
```
