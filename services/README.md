# VetrAI Platform Microservices

This directory contains all the microservices that power the VetrAI platform.

## Architecture Overview

VetrAI follows a microservices architecture with the following services:

### Core Services

1. **Auth Service** (`auth/`) - Port 8001
   - User authentication and authorization
   - JWT token management
   - User CRUD operations
   - Password reset and email verification

2. **Tenancy Service** (`tenancy/`) - Port 8002
   - Multi-tenant organization management
   - Organization CRUD operations
   - Tenant isolation and settings

### Feature Services

3. **API Keys Service** (`keys/`) - Port 8003
   - Secure API key generation with SHA256 hashing
   - Scoped permissions per key
   - Rate limiting integration
   - Key expiration and rotation
   - Usage tracking and analytics

4. **Billing Service** (`billing/`) - Port 8004
   - Stripe integration for payments
   - Subscription management
   - Invoice generation
   - Webhook processing
   - Usage-based billing

5. **Support Service** (`support/`) - Port 8005
   - Ticket management system
   - Comment threading
   - File attachment support (MinIO)
   - SLA tracking
   - Assignment workflows

6. **Themes Service** (`themes/`) - Port 8006
   - Organization-specific branding
   - Logo and favicon management
   - Color scheme customization
   - CSS generation for white-labeling
   - Theme preview

7. **Notifications Service** (`notifications/`) - Port 8007
   - Multi-channel notifications (email, in-app, SMS)
   - Template management
   - User preferences
   - Delivery queue with Celery
   - Notification history

8. **Workers Service** (`workers/`) - Port 8008
   - Background job processing
   - Celery integration
   - LangGraph workflow execution
   - Job monitoring and metrics
   - Retry mechanisms

### Shared Module

The `shared/` directory contains common utilities used across all services:

- **config/**: Configuration management and settings
- **middleware/**: Authentication and authorization middleware
- **models/**: Base database models
- **utils/**: Common utilities (database, security, etc.)

## Technology Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL with pgvector
- **Cache**: Redis
- **Storage**: MinIO (S3-compatible)
- **Queue**: Celery with Redis broker
- **Containerization**: Docker
- **Orchestration**: Docker Compose / Kubernetes

## Development Setup

### Prerequisites

- Python 3.11+
- Docker and Docker Compose
- PostgreSQL 15+ (or use Docker)
- Redis 7+ (or use Docker)

### Local Development

1. **Install dependencies:**
   ```bash
   # Install shared dependencies
   pip install -r services/shared/requirements.txt
   
   # Install service-specific dependencies
   pip install -r services/<service-name>/requirements.txt
   ```

2. **Set up environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Start infrastructure services:**
   ```bash
   docker-compose up -d postgres redis minio
   ```

4. **Run database migrations:**
   ```bash
   # Migrations are auto-applied via init.sql
   docker-compose exec postgres psql -U vetrai -d vetrai_db -f /docker-entrypoint-initdb.d/init.sql
   ```

5. **Start a service:**
   ```bash
   cd services/<service-name>
   uvicorn app.main:app --reload --port 8000
   ```

### Docker Development

Start all services with Docker Compose:

```bash
docker-compose up -d
```

View logs:
```bash
docker-compose logs -f <service-name>
```

## API Documentation

Each service provides interactive API documentation:

- **Keys Service**: http://localhost:8003/docs
- **Billing Service**: http://localhost:8004/docs
- **Support Service**: http://localhost:8005/docs
- **Themes Service**: http://localhost:8006/docs
- **Notifications Service**: http://localhost:8007/docs
- **Workers Service**: http://localhost:8008/docs

## Service Communication

Services communicate through:

1. **Direct HTTP calls**: For synchronous operations
2. **Shared database**: For data consistency
3. **Redis pub/sub**: For event-driven messaging
4. **Celery tasks**: For asynchronous operations

## Authentication & Authorization

All services use JWT-based authentication provided by the Auth service:

1. User logs in via Auth service
2. Auth service returns JWT access token
3. Client includes token in Authorization header: `Bearer <token>`
4. Services validate token using shared middleware

### API Key Authentication

For programmatic access, services support API key authentication:

1. Generate API key via Keys service
2. Include in requests: `X-API-Key: vetrai_<key>`
3. Keys service validates and tracks usage

## Multi-Tenancy

All services are multi-tenant aware:

- Each request is scoped to an organization
- Data isolation enforced at database and application level
- Organization ID derived from authenticated user/API key

## Rate Limiting

Rate limiting is implemented at multiple levels:

- Per API key (configurable per key)
- Per organization (based on plan)
- Per endpoint (using Redis)

## Error Handling

Standard error response format:

```json
{
  "detail": "Error message",
  "status_code": 400,
  "timestamp": "2024-01-01T00:00:00Z"
}
```

## Testing

Run tests for a service:

```bash
cd services/<service-name>
pytest tests/ -v --cov=app
```

Run tests for all services:

```bash
pytest services/*/tests/ -v --cov=services
```

## Code Quality

Format code:
```bash
black services/
isort services/
```

Lint code:
```bash
flake8 services/ --max-line-length=100 --exclude=__pycache__,venv,env
```

Type checking:
```bash
mypy services/ --ignore-missing-imports
```

Security scan:
```bash
bandit -r services/ -f json -o bandit-report.json
```

## Monitoring

Services expose metrics for monitoring:

- **Health check**: `GET /health`
- **Prometheus metrics**: `GET /metrics` (when enabled)
- **Grafana dashboards**: Available at http://localhost:3002

## Deployment

### Docker Compose (Development/Testing)

```bash
docker-compose up -d
```

### Kubernetes (Production)

Helm charts are available in `infra/helm/`:

```bash
helm install vetrai ./infra/helm/vetrai -f values.yaml
```

## Environment Variables

Key environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | - |
| `REDIS_URL` | Redis connection string | - |
| `JWT_SECRET_KEY` | Secret for JWT signing | - |
| `STRIPE_SECRET_KEY` | Stripe API secret key | - |
| `MINIO_ENDPOINT` | MinIO/S3 endpoint | - |
| `SMTP_HOST` | SMTP server for emails | - |
| `CELERY_BROKER_URL` | Celery broker URL | - |

See `.env.example` for complete list.

## Contributing

1. Create a feature branch
2. Make changes and add tests
3. Run code quality checks
4. Submit a pull request

## License

Copyright (c) 2024 VetrAI. All rights reserved.
