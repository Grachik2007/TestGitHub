# Architecture Overview

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        Client Layer                              │
├─────────────────────────────────────────────────────────────────┤
│  Next.js Dashboard  │  Telegram Bot  │  Mobile Apps              │
└──────────┬──────────────────────┬──────────────┬────────────────┘
           │                      │              │
┌──────────▼──────────────────────▼──────────────▼────────────────┐
│                   API Gateway / Load Balancer                    │
│                         (Nginx)                                  │
└──────────┬──────────────────────────────────────────────────────┘
           │
┌──────────▼──────────────────────────────────────────────────────┐
│                   FastAPI Backend Services                       │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ Authentication & Authorization                           │   │
│  │ - JWT Auth                                              │   │
│  │ - RBAC                                                  │   │
│  │ - User Management                                       │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ Multi-Agent Orchestration Layer                         │   │
│  │ ┌─────────────────────────────────────────────────────┐ │   │
│  │ │ Agent Dispatcher & Router                           │ │   │
│  │ ├─────────────────────────────────────────────────────┤ │   │
│  │ │ SEO Agent  │ Supplier Agent  │ Product Agent  │     │ │   │
│  │ │ Pricing Agent                                       │ │   │
│  │ └─────────────────────────────────────────────────────┘ │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ Business Logic Services                                 │   │
│  │ - User Service                                          │   │
│  │ - Agent Service                                         │   │
│  │ - Analytics Service                                     │   │
│  │ - Billing Service                                       │   │
│  │ - Webhook Service                                       │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                  │
└──────────┬──────────────────────────────────────────────────────┘
           │
┌──────────▼──────────────────────────────────────────────────────┐
│              Data & Caching Layer                                │
├──────────────────────────────────────────────────────────────────┤
│  PostgreSQL  │  Redis  │  LangChain Memory  │  Vector DB        │
└─────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────┐
│              Background Job Processing                          │
├────────────────────────────────────────────────────────────────┤
│  Celery Workers  │  Celery Beat Scheduler                       │
└────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────┐
│              External Services Integration                      │
├────────────────────────────────────────────────────────────────┤
│  OpenAI API  │  Stripe  │  Telegram  │  Email Service          │
└────────────────────────────────────────────────────────────────┘
```

## Backend Architecture (FastAPI)

### Project Structure

```
apps/api/
├── main.py                 # FastAPI application entry point
├── Dockerfile              # Docker configuration
├── requirements.txt        # Python dependencies
├── .env.example            # Environment variables template
│
├── core/
│   ├── config.py          # Configuration settings
│   ├── security.py        # JWT, encryption, auth utils
│   ├── dependencies.py    # Shared dependencies
│   └── constants.py       # Application constants
│
├── models/
│   ├── __init__.py
│   ├── user.py            # User model
│   ├── agent.py           # Agent model
│   ├── task.py            # Task/Job model
│   ├── conversation.py    # Conversation history
│   ├── subscription.py    # Billing & subscription
│   └── audit_log.py       # Audit logging
│
├── schemas/
│   ├── __init__.py
│   ├── user.py            # User request/response schemas
│   ├── agent.py           # Agent schemas
│   ├── task.py            # Task schemas
│   └── common.py          # Common schemas
│
├── repositories/
│   ├── __init__.py
│   ├── base.py            # Base repository class
│   ├── user_repo.py       # User repository
│   ├── agent_repo.py      # Agent repository
│   ├── task_repo.py       # Task repository
│   └── subscription_repo.py
│
├── services/
│   ├── __init__.py
│   ├── user_service.py    # User business logic
│   ├── agent_service.py   # Agent orchestration
│   ├── task_service.py    # Task processing
│   ├── auth_service.py    # Authentication
│   ├── billing_service.py # Stripe integration
│   ├── email_service.py   # Email sending
│   └── analytics_service.py
│
├── api/
│   ├── __init__.py
│   ├── v1/
│   │   ├── __init__.py
│   │   ├── endpoints/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py          # Login, register, refresh
│   │   │   ├── users.py         # User management
│   │   │   ├── agents.py        # Agent operations
│   │   │   ├── tasks.py         # Task management
│   │   │   ├── analytics.py     # Analytics endpoint
│   │   │   ├── billing.py       # Billing operations
│   │   │   └── health.py        # Health checks
│   │   └── dependencies.py      # API dependencies
│   └── webhooks/
│       ├── __init__.py
│       ├── stripe.py            # Stripe webhooks
│       └── telegram.py          # Telegram webhooks
│
├── agents/
│   ├── __init__.py
│   ├── base_agent.py      # Base agent class
│   ├── dispatcher.py      # Agent dispatcher/router
│   ├── orchestrator.py    # Multi-agent orchestration
│   │
│   ├── seo/
│   │   ├── __init__.py
│   │   ├── agent.py       # SEO agent implementation
│   │   ├── tools.py       # SEO-specific tools
│   │   └── prompts.py     # SEO prompt templates
│   │
│   ├── supplier/
│   │   ├── __init__.py
│   │   ├── agent.py
│   │   ├── tools.py
│   │   └── prompts.py
│   │
│   ├── product/
│   │   ├── __init__.py
│   │   ├── agent.py
│   │   ├── tools.py
│   │   └── prompts.py
│   │
│   └── pricing/
│       ├── __init__.py
│       ├── agent.py
│       ├── tools.py
│       └── prompts.py
│
├── tools/
│   ├── __init__.py
│   ├── web_search.py      # Web search tool
│   ├── data_analysis.py   # Data analysis tools
│   ├── calculator.py      # Calculation tools
│   ├── comparison.py      # Comparison tools
│   └── knowledge_base.py  # Knowledge base access
│
├── memory/
│   ├── __init__.py
│   ├── conversation_memory.py
│   ├── user_memory.py     # User preferences/history
│   ├── cache_manager.py   # Redis cache management
│   └── vector_store.py    # Vector embeddings storage
│
├── tasks/
│   ├── __init__.py
│   ├── celery_app.py      # Celery configuration
│   ├── agent_tasks.py     # Agent execution tasks
│   ├── email_tasks.py     # Email sending tasks
│   ├── analytics_tasks.py # Analytics computation tasks
│   └── webhook_tasks.py   # Webhook processing
│
├── middleware/
│   ├── __init__.py
│   ├── error_handler.py   # Global error handling
│   ├── auth_middleware.py # JWT validation
│   ├── rate_limit.py      # Rate limiting
│   └── logging.py         # Request/response logging
│
├── utils/
│   ├── __init__.py
│   ├── validators.py      # Input validation
│   ├── formatters.py      # Response formatting
│   ├── logger.py          # Logging setup
│   ├── exceptions.py      # Custom exceptions
│   └── helpers.py         # Helper utilities
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py        # Pytest fixtures
│   ├── test_auth.py
│   ├── test_agents.py
│   ├── test_services.py
│   └── test_api.py
│
├── migrations/
│   ├── versions/          # Alembic migrations
│   └── env.py
│
└── logs/
    └── app.log
```

### Key Design Patterns

1. **Repository Pattern**: Data access abstraction
2. **Service Layer**: Business logic encapsulation
3. **Dependency Injection**: Loose coupling
4. **Factory Pattern**: Agent creation
5. **Observer Pattern**: Event handling
6. **Chain of Responsibility**: Middleware stack

## Frontend Architecture (Next.js)

### Project Structure

```
apps/web/
├── app/
│   ├── layout.tsx         # Root layout
│   ├── page.tsx           # Home page
│   │
│   ├── (auth)/
│   │   ├── login/page.tsx
│   │   ├── register/page.tsx
│   │   └── reset/page.tsx
│   │
│   ├── (dashboard)/
│   │   ├── layout.tsx     # Dashboard layout
│   │   ├── page.tsx       # Dashboard home
│   │   │
│   │   ├── agents/
│   │   │   ├── page.tsx           # Agents list
│   │   │   ├── [id]/page.tsx      # Agent details
│   │   │   └── [id]/chat/page.tsx # Agent chat
│   │   │
│   │   ├── analytics/
│   │   │   └── page.tsx
│   │   │
│   │   ├── billing/
│   │   │   ├── page.tsx
│   │   │   └── invoice/[id].tsx
│   │   │
│   │   ├── settings/
│   │   │   ├── page.tsx
│   │   │   ├── profile/page.tsx
│   │   │   ├── security/page.tsx
│   │   │   └── api-keys/page.tsx
│   │   │
│   │   └── admin/
│   │       ├── page.tsx
│   │       ├── users/page.tsx
│   │       └── analytics/page.tsx
│   │
│   └── api/
│       └── auth/callback/route.ts
│
├── components/
│   ├── layout/
│   │   ├── Navbar.tsx
│   │   ├── Sidebar.tsx
│   │   ├── Footer.tsx
│   │   └── DashboardLayout.tsx
│   │
│   ├── agents/
│   │   ├── AgentCard.tsx
│   │   ├── AgentChat.tsx
│   │   ├── AgentList.tsx
│   │   ├── AgentDetails.tsx
│   │   └── AgentHistory.tsx
│   │
│   ├── analytics/
│   │   ├── AnalyticsChart.tsx
│   │   ├── StatsCard.tsx
│   │   ├── UsageMetrics.tsx
│   │   └── ActivityTimeline.tsx
│   │
│   ├── auth/
│   │   ├── LoginForm.tsx
│   │   ├── RegisterForm.tsx
│   │   └── ProtectedRoute.tsx
│   │
│   ├── ui/
│   │   ├── Button.tsx
│   │   ├── Input.tsx
│   │   ├── Card.tsx
│   │   ├── Modal.tsx
│   │   ├── Loading.tsx
│   │   ├── Toast.tsx
│   │   └── Pagination.tsx
│   │
│   └── common/
│       ├── Theme.tsx
│       ├── ErrorBoundary.tsx
│       └── Loading.tsx
│
├── hooks/
│   ├── useAuth.ts
│   ├── useApi.ts
│   ├── useTheme.ts
│   ├── useLocalStorage.ts
│   ├── useDebounce.ts
│   └── useInfiniteScroll.ts
│
├── store/
│   ├── auth.ts            # Zustand auth store
│   ├── agents.ts          # Agents state
│   ├── ui.ts              # UI state
│   └── notifications.ts   # Notifications
│
├── services/
│   ├── api.ts             # API client (axios/fetch)
│   ├── auth.ts            # Auth service
│   ├── agents.ts          # Agent service
│   ├── analytics.ts       # Analytics service
│   └── storage.ts         # Local storage service
│
├── lib/
│   ├── constants.ts
│   ├── utils.ts
│   ├── formatters.ts
│   ├── validators.ts
│   └── classNames.ts
│
├── styles/
│   ├── globals.css
│   ├── variables.css
│   └── animations.css
│
├── public/
│   ├── icons/
│   ├── images/
│   └── fonts/
│
├── tests/
│   ├── components/
│   ├── hooks/
│   ├── services/
│   └── __mocks__/
│
├── next.config.js
├── tailwind.config.js
├── tsconfig.json
└── package.json
```

## Telegram Bot Architecture

```
apps/telegram/
├── main.py                # Bot entry point
├── Dockerfile
├── requirements.txt
│
├── handlers/
│   ├── __init__.py
│   ├── start.py          # /start command
│   ├── agents.py         # Agent commands
│   ├── help.py           # /help command
│   └── callbacks.py      # Inline button callbacks
│
├── services/
│   ├── __init__.py
│   ├── api_client.py     # Communication with backend
│   ├── agent_service.py  # Agent interaction
│   └── user_service.py   # User management
│
├── utils/
│   ├── __init__.py
│   ├── formatters.py     # Message formatting
│   ├── keyboards.py      # Inline keyboards
│   └── constants.py      # Constants
│
└── models/
    ├── __init__.py
    ├── user.py
    └── conversation.py
```

## Data Models

### Core Models Diagram

```
User (1) ──────────────────┐
                           │
                  ┌────────▼─────────┐
                  │ Subscription     │
                  │ (Stripe)         │
                  └──────────────────┘

User (1) ──────── N ──── Task
         ├─────── N ──── Conversation
         └─────── N ──── AuditLog

Agent (1) ──────── N ──── AgentExecution
         ├─────── N ──── AgentMetrics
         └─────── N ──── ToolUsage

Conversation (1) ──────── N ──── Message
               ├─────── 1 ──── Agent
               └─────── 1 ──── User
```

## Data Flow

### Agent Execution Flow

```
User Input
   │
   ▼
FastAPI Endpoint
   │
   ▼
Authentication & Validation
   │
   ▼
Agent Dispatcher
   │
   ├─► SEO Agent ──┐
   ├─► Supplier Agent ─┤
   ├─► Product Agent ──┼─► Tools Execution
   └─► Pricing Agent ──┘
   │
   ▼
LangChain/LangGraph Processing
   │
   ▼
External Tools Integration
   (Web Search, Data Analysis, etc.)
   │
   ▼
Response Generation
   │
   ▼
Caching (Redis)
   │
   ▼
Database Storage
   │
   ▼
Response to User
```

## Technology Stack Details

### Backend Stack

- **Framework**: FastAPI 0.104+
- **ORM**: SQLAlchemy 2.0+
- **Database**: PostgreSQL 15+
- **Cache**: Redis 7+
- **Task Queue**: Celery 5.3+
- **API Documentation**: FastAPI Swagger + ReDoc
- **Validation**: Pydantic v2
- **Authentication**: Python-JWT
- **Background Jobs**: Celery
- **HTTP Client**: HTTPX, aiohttp
- **Email**: Starlette-mail
- **Payment**: Stripe API
- **LLM Framework**: LangChain, LangGraph
- **Bot Framework**: python-telegram-bot
- **Testing**: Pytest, Pytest-asyncio
- **Linting**: Black, Flake8, Pylint
- **Type Checking**: Mypy

### Frontend Stack

- **Framework**: Next.js 15
- **Language**: TypeScript
- **Styling**: TailwindCSS
- **UI Components**: shadcn/ui
- **Animations**: Framer Motion
- **State Management**: Zustand
- **Data Fetching**: React Query (TanStack Query)
- **API Client**: Axios / Fetch API
- **Forms**: React Hook Form
- **Validation**: Zod
- **Charts**: Recharts / Chart.js
- **Icons**: Lucide React
- **Testing**: Jest, React Testing Library
- **Linting**: ESLint
- **Formatting**: Prettier

## Security Architecture

```
┌─ Input Validation (Pydantic)
│
├─ CORS Protection
│
├─ Rate Limiting (per user, per IP)
│
├─ JWT Authentication
│   └─ Token rotation
│   └─ Refresh tokens
│
├─ RBAC Authorization
│   ├─ Admin
│   ├─ User
│   └─ Guest
│
├─ Environment Secrets
│   └─ No hardcoded credentials
│
├─ HTTPS/TLS
│   └─ Certificate management
│
├─ SQL Injection Prevention
│   └─ Parameterized queries
│
├─ XSS Prevention
│   └─ Input sanitization
│
├─ CSRF Protection
│   └─ Token validation
│
└─ Audit Logging
    └─ All sensitive operations tracked
```

## Deployment Architecture

```
┌──────────────────────────────────────────────────────┐
│                 Cloudflare CDN                        │
└────────────┬─────────────────────────────────────────┘
             │
┌────────────▼─────────────────────────────────────────┐
│              Load Balancer (Nginx)                    │
├─────────────────────────────────────────────────────┤
│ - SSL Termination                                   │
│ - Request Routing                                   │
│ - Compression                                       │
└────────────┬─────────────────────────────────────────┘
             │
    ┌────────┴────────┬──────────────────┐
    │                 │                  │
┌───▼──┐     ┌──────▼──┐      ┌────────▼───┐
│ API  │     │   Web   │      │  Telegram  │
│Pods  │     │  Pods   │      │   Service  │
└──┬───┘     └────┬────┘      └────┬───────┘
   │              │                │
   └──────────────┴────────────────┘
                  │
       ┌──────────┴──────────┐
       │                     │
    ┌──▼──┐          ┌──────▼────┐
    │ DB  │          │  Cache    │
    └─────┘          │  (Redis)  │
                     └───────────┘
```

## Scaling Strategy

1. **Horizontal Scaling**: Multiple API instances behind load balancer
2. **Database Replication**: Read replicas for analytics queries
3. **Caching Layer**: Redis for session and data caching
4. **CDN**: Cloudflare for static assets
5. **Celery Workers**: Scale based on task queue depth
6. **Containerization**: Docker for consistent deployment

## Monitoring & Observability

- **Logging**: Centralized logging with ELK stack / CloudWatch
- **Metrics**: Prometheus metrics
- **Tracing**: OpenTelemetry for distributed tracing
- **Alerting**: Real-time alerts for critical issues
- **Uptime Monitoring**: Status page

## API Versioning Strategy

- Current: `/api/v1/`
- URL-based versioning
- Backwards compatible changes maintain support
- Deprecation warnings 6 months before removal
