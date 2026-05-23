# AI Business SaaS Agents Platform

Modern production-ready AI SaaS platform with multi-agent orchestration, Telegram assistant, and analytics dashboard.

## 🚀 Features

- **Multi-Agent System**: SEO, Supplier, Product Research, and Pricing agents
- **Telegram AI Assistant**: Full-featured bot with agent integration
- **Analytics Dashboard**: Real-time analytics and agent monitoring
- **Enterprise Architecture**: Clean, scalable, modular design
- **Production Ready**: Docker, CI/CD, monitoring, logging
- **Modern Tech Stack**: Next.js, FastAPI, LangGraph, PostgreSQL

## 📦 Project Structure

```
apps/
  ├── web/              # Next.js dashboard frontend
  ├── api/              # FastAPI backend
  └── telegram/         # Telegram bot service

packages/
  ├── ui/               # Shared UI components
  ├── agents/           # AI agents implementation
  ├── shared/           # Shared utilities and types
  └── config/           # Configuration management

infrastructure/
  ├── docker/           # Docker configurations
  ├── nginx/            # Nginx configs
  └── scripts/          # Deployment scripts
```

## 🛠️ Tech Stack

### Frontend
- Next.js 15 with TypeScript
- TailwindCSS + shadcn/ui
- Framer Motion animations
- Zustand state management
- React Query for data fetching

### Backend
- FastAPI with Python 3.11+
- LangChain + LangGraph
- Pydantic validation
- PostgreSQL database
- Redis caching
- Celery for task processing

### AI & Agents
- OpenAI API integration
- Multi-agent orchestration
- Memory and context management
- RAG-ready architecture
- Tool system

### Infrastructure
- Docker & Docker Compose
- GitHub Actions CI/CD
- Cloudflare integration
- Production deployment configs

## 🚀 Quick Start

### Prerequisites
- Node.js 20+
- Python 3.11+
- PostgreSQL
- Redis
- Docker & Docker Compose

### Setup

1. **Clone repository**
```bash
git clone git@github.com:Grachik2007/TestGitHub.git
cd TestGitHub
```

2. **Setup backend**
```bash
cd apps/api
pip install -r requirements.txt
cp .env.example .env
python -m alembic upgrade head
```

3. **Setup frontend**
```bash
cd apps/web
npm install
cp .env.example .env.local
```

4. **Setup Telegram bot**
```bash
cd apps/telegram
pip install -r requirements.txt
cp .env.example .env
```

5. **Run with Docker Compose**
```bash
docker-compose up -d
```

## 📖 Documentation

- [Backend API Documentation](./apps/api/README.md)
- [Frontend Development](./apps/web/README.md)
- [Telegram Bot Guide](./apps/telegram/README.md)
- [Architecture Overview](./ARCHITECTURE.md)
- [Deployment Guide](./DEPLOYMENT.md)

## 🤖 AI Agents

### 1. SEO Agent
- Keyword clustering and analysis
- SEO article generation
- Metadata optimization
- Competitor analysis

### 2. Supplier Agent
- Supplier comparison and filtering
- Pricing analysis
- Sourcing recommendations
- Margin calculations

### 3. Product Agent
- Trend analysis
- Profitable product discovery
- Niche identification
- Market validation

### 4. Pricing Agent
- Price optimization
- Profitability calculations
- Competitor pricing analysis
- Recommendations

## 📊 Dashboard Features

- Real-time analytics
- Agent monitoring
- Usage tracking
- Billing management
- User management
- Dark/Light theme
- Mobile responsive

## 🔐 Security

- JWT authentication
- RBAC (Role-Based Access Control)
- Rate limiting
- Input validation
- CORS protection
- Environment-based secrets
- Audit logging

## 💳 Billing

- Stripe integration
- Usage-based pricing
- Subscription management
- Invoice generation
- Credits system

## 🚢 Deployment

- Docker containers
- Docker Compose orchestration
- GitHub Actions CI/CD
- Environment configurations
- Health checks
- Monitoring ready

## 📝 License

MIT

## 👥 Author

Created with ❤️ by Senior AI Architecture Team