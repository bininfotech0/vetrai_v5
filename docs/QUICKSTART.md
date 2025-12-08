# VetrAI Platform - Quick Start Guide

## 🚀 Get Started in 5 Minutes

This guide will help you get the VetrAI platform running locally with all 8 microservices.

## Prerequisites

- Docker Desktop (with Docker Compose)
- Git
- 8GB RAM minimum
- 10GB disk space

## Step 1: Clone the Repository

```bash
git clone https://github.com/bininfotech0/vetrai_v5.git
cd vetrai_v5
```

## Step 2: Configure Environment

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and set required values:
# - JWT_SECRET_KEY (generate with: openssl rand -hex 32)
# - STRIPE_SECRET_KEY (optional, for billing)
# - SMTP credentials (optional, for email notifications)
```

## Step 3: Start All Services

```bash
# Start all services with Docker Compose
docker-compose up -d

# Check service status
docker-compose ps

# View logs
docker-compose logs -f
```

This will start:
- ✅ PostgreSQL (with pgvector)
- ✅ Redis
- ✅ MinIO
- ✅ 8 Microservices (auth, tenancy, keys, billing, support, themes, notifications, workers)
- ✅ Prometheus
- ✅ Grafana
- ✅ Celery Worker

## Step 4: Initialize Database

```bash
# Run database migrations
./scripts/setup/migrate.sh

# Or manually:
docker-compose exec postgres psql -U vetrai -d vetrai_db -f /docker-entrypoint-initdb.d/init.sql
```

## Step 5: Verify Services

### Health Checks

All services expose health endpoints:

```bash
# Auth Service
curl http://localhost:8001/health

# Tenancy Service
curl http://localhost:8002/health

# Keys Service
curl http://localhost:8003/health

# Billing Service
curl http://localhost:8004/health

# Support Service
curl http://localhost:8005/health

# Themes Service
curl http://localhost:8006/health

# Notifications Service
curl http://localhost:8007/health

# Workers Service
curl http://localhost:8008/health
```

### API Documentation

Access Swagger UI for each service:

- Auth: http://localhost:8001/docs
- Tenancy: http://localhost:8002/docs
- Keys: http://localhost:8003/docs
- Billing: http://localhost:8004/docs
- Support: http://localhost:8005/docs
- Themes: http://localhost:8006/docs
- Notifications: http://localhost:8007/docs
- Workers: http://localhost:8008/docs

## Step 6: Test the Platform

### Create Your First User

```bash
curl -X POST http://localhost:8001/api/v1/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "Test@123456",
    "first_name": "Test",
    "last_name": "User",
    "organization_id": 1
  }'
```

### Login

```bash
curl -X POST http://localhost:8001/api/v1/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "Test@123456"
  }'
```

Save the `access_token` from the response.

### Test Protected Endpoints

```bash
# Get current user info
curl -X GET http://localhost:8001/api/v1/me \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"

# List organizations
curl -X GET http://localhost:8002/api/v1/organizations \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"

# Create API key
curl -X POST http://localhost:8003/api/v1/keys \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My First API Key",
    "scopes": ["read", "write"]
  }'
```

## Step 7: Access Monitoring

### Prometheus

Access metrics: http://localhost:9090

### Grafana

Access dashboards: http://localhost:3002
- Default credentials: `admin` / `admin`

### MinIO Console

Access storage: http://localhost:9001
- Credentials: `vetrai_minio_access` / `vetrai_minio_secret`

## Common Tasks

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f auth-service

# Last 100 lines
docker-compose logs --tail=100 auth-service
```

### Restart a Service

```bash
docker-compose restart auth-service
```

### Stop All Services

```bash
docker-compose down
```

### Stop and Remove Volumes (Clean Start)

```bash
docker-compose down -v
```

### Run Database Queries

```bash
# Connect to PostgreSQL
docker-compose exec postgres psql -U vetrai -d vetrai_db

# Example queries
SELECT * FROM users;
SELECT * FROM organizations;
SELECT * FROM api_keys;
```

### Access Redis

```bash
# Connect to Redis CLI
docker-compose exec redis redis-cli

# Example commands
KEYS *
GET some_key
```

## Development Workflow

### Run Individual Service Locally

```bash
cd services/auth
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8001
```

### Run Tests

```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run tests
pytest services/auth/tests/
```

### Format Code

```bash
# Install formatters
pip install black isort

# Format
black services/
isort services/
```

## Troubleshooting

### Port Already in Use

If ports are already in use, modify `docker-compose.yml` to use different ports:

```yaml
auth-service:
  ports:
    - "8101:8000"  # Change 8001 to 8101
```

### Database Connection Failed

Check if PostgreSQL is running:

```bash
docker-compose ps postgres
docker-compose logs postgres
```

### Service Won't Start

Check logs for errors:

```bash
docker-compose logs auth-service
```

Common issues:
- Missing environment variables
- Database not initialized
- Port conflicts

### Clear Docker Cache

```bash
docker-compose down -v
docker system prune -a
docker-compose up -d --build
```

## Next Steps

1. Read the [Services Documentation](SERVICES.md) for detailed API information
2. Review [Architecture Guide](architecture/README.md) to understand the system design
3. Check [Security Guide](guides/security.md) for security best practices
4. See [Deployment Guide](deployment/README.md) for production deployment

## Default Credentials

The platform creates a default super admin user:

- **Email**: admin@vetrai.io
- **Password**: Admin@123

⚠️ **Important**: Change this password immediately in production!

## Support

- Documentation: [docs.vetrai.io](https://docs.vetrai.io)
- Issues: [GitHub Issues](https://github.com/bininfotech0/vetrai_v5/issues)
- Email: support@vetrai.io

## What's Next?

Now that you have the platform running:

1. Explore the API documentation at each service's `/docs` endpoint
2. Try creating organizations, API keys, and support tickets
3. Customize themes for your organization
4. Set up billing with Stripe
5. Configure email notifications
6. Create workflow jobs

Happy building! 🚀
