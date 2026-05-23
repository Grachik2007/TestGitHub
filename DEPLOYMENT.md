# Deployment Guide

Guide for deploying AI Agents Platform to production.

## Prerequisites

- Docker & Docker Compose
- PostgreSQL 15+
- Redis 7+
- Node.js 20+ (for local development)
- Python 3.11+ (for local development)

## Local Development Setup

### Quick Start with Docker Compose

```bash
# Clone repository
git clone git@github.com:Grachik2007/TestGitHub.git
cd TestGitHub

# Setup environment
./infrastructure/scripts/setup.sh

# Edit .env files as needed
vim .env
vim apps/api/.env
vim apps/web/.env.local
vim apps/telegram/.env

# Start all services
docker-compose up -d

# View logs
docker-compose logs -f
```

### Manual Local Setup

1. **Backend (FastAPI)**
```bash
cd apps/api
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python -m uvicorn main:app --reload
```

2. **Frontend (Next.js)**
```bash
cd apps/web
npm install
cp .env.example .env.local
npm run dev
```

3. **Telegram Bot**
```bash
cd apps/telegram
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python main.py
```

## Production Deployment

### Option 1: Docker Compose

```bash
./infrastructure/scripts/deploy.sh production
```

### Option 2: Railway

1. Connect GitHub repository to Railway
2. Configure environment variables
3. Deploy automatically on push

```
Variables needed:
- DATABASE_URL: PostgreSQL connection
- REDIS_URL: Redis connection
- OPENAI_API_KEY: OpenAI API key
- JWT_SECRET_KEY: Secure random string
- STRIPE_SECRET_KEY: Stripe secret
- TELEGRAM_BOT_TOKEN: Telegram token
```

### Option 3: Render

1. Create new Web Service from GitHub
2. Select repository
3. Configure:
   - Build Command: `docker-compose build`
   - Start Command: `docker-compose up`
4. Add environment variables (same as Railway)

### Option 4: VPS (Nginx + Docker)

1. **Install Docker**
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
```

2. **Clone and setup**
```bash
git clone git@github.com:Grachik2007/TestGitHub.git
cd TestGitHub
./infrastructure/scripts/setup.sh
```

3. **Configure DNS**
- Point your domain to VPS IP
- Update CORS_ORIGINS in .env

4. **Deploy**
```bash
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

5. **Setup SSL (Let's Encrypt)**
```bash
docker run --rm -it -v /etc/letsencrypt:/etc/letsencrypt \
  -v /var/lib/letsencrypt:/var/lib/letsencrypt \
  -p 80:80 -p 443:443 \
  certbot/certbot certonly -d yourdomain.com
```

## Environment Variables

### Required
```
DATABASE_URL=postgresql://user:password@host:5432/db
REDIS_URL=redis://host:6379/0
OPENAI_API_KEY=sk-...
JWT_SECRET_KEY=your-secret-key
```

### Optional
```
STRIPE_SECRET_KEY=sk_...
TELEGRAM_BOT_TOKEN=...
SENTRY_DSN=...
```

## Database Migrations

```bash
# Create migration
docker-compose exec api alembic revision --autogenerate -m "description"

# Apply migrations
docker-compose exec api alembic upgrade head

# Rollback
docker-compose exec api alembic downgrade -1
```

## Health Checks

```bash
# API health
curl http://localhost:8000/health

# API readiness
curl http://localhost:8000/ready

# Web health (via browser)
http://localhost:3000

# Check all services
docker-compose ps
```

## Monitoring

### Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f api

# API logs
docker-compose exec api tail -f logs/app.log
```

### Database
```bash
# Connect to PostgreSQL
docker-compose exec db psql -U ai_user -d ai_agents

# Common queries
\dt                 # List tables
\l                  # List databases
SELECT * FROM users; # Query users
```

### Redis
```bash
# Connect to Redis
docker-compose exec redis redis-cli -a redis_password_dev

# Common commands
KEYS *              # List all keys
GET key             # Get value
FLUSHDB             # Clear database
```

## Backup & Restore

### PostgreSQL Backup
```bash
docker-compose exec db pg_dump -U ai_user ai_agents > backup.sql

# Restore
docker-compose exec -T db psql -U ai_user ai_agents < backup.sql
```

### Redis Backup
```bash
docker-compose exec redis redis-cli -a redis_password_dev SAVE
docker cp ai_agents_redis:/data/dump.rdb ./redis-backup.rdb
```

## Scaling

### Multiple API Instances
```yaml
# docker-compose.yml
api-1:
  build: ./apps/api
  ...

api-2:
  build: ./apps/api
  ...

# Then route traffic through Nginx
```

### Database Read Replicas
```bash
# Setup PostgreSQL replication
# See PostgreSQL documentation for streaming replication
```

### Redis Cluster
```bash
# Setup Redis Sentinel for high availability
# See Redis documentation for cluster setup
```

## Troubleshooting

### Services won't start
```bash
# Check logs
docker-compose logs

# Restart services
docker-compose restart

# Rebuild containers
docker-compose down
docker-compose up --build
```

### Database connection issues
```bash
# Check database is running
docker-compose ps db

# Test connection
docker-compose exec api psql $DATABASE_URL
```

### API errors
```bash
# Check API logs
docker-compose logs api

# Connect to container
docker-compose exec api bash
```

### Memory issues
```bash
# Check container stats
docker stats

# Increase Docker memory limit
# Edit Docker Desktop settings or daemon.json
```

## Performance Tuning

### Database
```
- Add indexes on frequently queried columns
- Enable connection pooling
- Configure vacuum settings
```

### Cache
```
- Increase Redis memory
- Set appropriate TTLs
- Use Redis compression
```

### API
```
- Enable gzip compression
- Optimize query N+1 problems
- Use connection pooling
- Profile slow endpoints
```

## Cloudflare Integration

1. **Add DNS records**
   - Type A: yourdomain.com -> VPS IP
   - Type CNAME: www -> yourdomain.com

2. **Enable SSL/TLS**
   - Flexible (Orange Cloud)
   - Full (Yellow Cloud + self-signed cert)
   - Full (Strict) (Yellow Cloud + valid cert)

3. **Configure Page Rules**
   - Cache level: Cache Everything
   - Browser TTL: 30 minutes

## Monitoring & Alerting

### Sentry Setup
```bash
# Add to .env
SENTRY_DSN=https://...@sentry.io/...

# Errors automatically tracked
```

### Health Checks
```
# Setup monitoring service to check:
- API health endpoint
- Web availability
- Database connectivity
- Redis connectivity
```

## Security Checklist

- [ ] Change default JWT_SECRET_KEY
- [ ] Use HTTPS only
- [ ] Enable CORS properly
- [ ] Set strong database password
- [ ] Rotate API keys regularly
- [ ] Enable firewall rules
- [ ] Setup log aggregation
- [ ] Regular security audits

## Support

For issues and deployment help, see:
- GitHub Issues: https://github.com/Grachik2007/TestGitHub/issues
- Documentation: ./ARCHITECTURE.md
