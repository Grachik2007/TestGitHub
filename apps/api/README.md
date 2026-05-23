# FastAPI Backend

Production-grade FastAPI backend for AI Agents Platform.

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- PostgreSQL 15+
- Redis 7+

### Setup

1. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Setup environment**
```bash
cp .env.example .env
# Edit .env with your settings
```

4. **Initialize database** (when ready with migrations)
```bash
python -m alembic upgrade head
```

5. **Run development server**
```bash
uvicorn main:app --reload
```

Server will be available at: `http://localhost:8000`
API docs: `http://localhost:8000/api/docs`

## 📁 Project Structure

- `main.py` - FastAPI application entry point
- `core/` - Configuration and core utilities
- `api/v1/` - API endpoints
- `models/` - Database models (SQLAlchemy)
- `schemas/` - Pydantic request/response schemas
- `services/` - Business logic
- `agents/` - AI agent implementations
- `tasks/` - Celery task definitions
- `middleware/` - Custom middleware

## 🔗 API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login user
- `POST /api/v1/auth/refresh` - Refresh access token

### Agents
- `GET /api/v1/agents` - List agents
- `POST /api/v1/agents/{id}/execute` - Execute agent task
- `GET /api/v1/agents/{id}/tasks` - Get task history

### Analytics
- `GET /api/v1/analytics` - Get analytics data
- `GET /api/v1/analytics/usage` - Usage metrics

### Billing
- `GET /api/v1/billing/plans` - Get subscription plans
- `GET /api/v1/billing/subscription` - Get user subscription

## 🤖 AI Agents

Implemented agents:
- **SEO Agent** - Keyword analysis, article generation
- **Supplier Agent** - Supplier comparison, pricing analysis
- **Product Agent** - Trend analysis, niche discovery
- **Pricing Agent** - Price optimization, profitability analysis

## 🔐 Security

- JWT authentication
- Password hashing with bcrypt
- CORS protection
- Rate limiting
- Input validation with Pydantic

## 📊 Database

Models:
- `User` - User accounts
- `Agent` - Agent configurations
- `Task` - Task executions
- `Conversation` - Chat history
- `Subscription` - Billing information

## 🚀 Deployment

### Docker
```bash
docker build -t ai-agents-api .
docker run -p 8000:8000 ai-agents-api
```

### Docker Compose
```bash
docker-compose up api
```

## 🧪 Testing

```bash
pytest
pytest --cov=.  # With coverage
pytest -v       # Verbose
```

## 📝 Development

### Code Style
- Black for formatting
- isort for imports
- Flake8 for linting

```bash
black .
isort .
flake8 .
```

### Type Checking
```bash
mypy .
```

## 📚 Documentation

- OpenAPI Docs: `/api/docs`
- ReDoc: `/api/redoc`
- OpenAPI JSON: `/api/openapi.json`

## 🔄 Background Tasks

Using Celery for:
- Agent execution
- Email sending
- Analytics computation
- Report generation

## 🛠️ Configuration

All configuration via environment variables in `.env` file.

See `.env.example` for all available options.

## 📞 Support

For issues and feature requests, please open an issue on GitHub.

## 📝 License

MIT
