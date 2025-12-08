# VetrAI Platform - Quick Start Guide

Get up and running with VetrAI Platform in less than 10 minutes!

## Prerequisites

Before you begin, ensure you have the following installed:

- **Docker** (20.10+) and **Docker Compose** (2.0+)
- **Git** (2.0+)
- **Python** 3.11+ (optional, for local development)
- **Node.js** 18+ (optional, for frontend development)

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/bininfotech0/vetrai_v5.git
cd vetrai_v5
```

### 2. Configure Environment Variables

Copy the example environment file and customize it:

```bash
cp .env.example .env
```

Edit `.env` file with your preferred text editor:

```bash
# Minimal required changes for local development:
nano .env  # or vim, code, etc.
```

**Important settings to review:**

```env
# Database
DATABASE_URL=postgresql://vetrai:vetrai_password@postgres:5432/vetrai_db

# JWT Secret (change this!)
JWT_SECRET_KEY=your-super-secret-jwt-key-change-me

# Admin User
ADMIN_EMAIL=admin@vetrai.io
ADMIN_PASSWORD=change-this-password
```

### 3. Start the Platform

Start all services using Docker Compose:

```bash
docker-compose up -d
```

This will start:
- PostgreSQL (database)
- Redis (cache/queue)
- MinIO (object storage)
- All microservices
- Prometheus (monitoring)
- Grafana (dashboards)

### 4. Initialize Database

Wait for PostgreSQL to be ready, then run migrations:

```bash
# Check if PostgreSQL is ready
docker-compose logs postgres

# Run database initialization
./scripts/setup/migrate.sh
```

### 5. Verify Installation

Check that all services are running:

```bash
docker-compose ps
```

Expected output:
```
NAME                   STATUS   PORTS
vetrai-auth            Up       0.0.0.0:8001->8000/tcp
vetrai-tenancy         Up       0.0.0.0:8002->8000/tcp
vetrai-postgres        Up       0.0.0.0:5432->5432/tcp
vetrai-redis           Up       0.0.0.0:6379->6379/tcp
vetrai-minio           Up       0.0.0.0:9000-9001->9000-9001/tcp
...
```

## Access the Platform

### API Endpoints

- **Authentication Service**: http://localhost:8001/docs
- **Tenancy Service**: http://localhost:8002/docs
- **API Keys Service**: http://localhost:8003/docs
- **Billing Service**: http://localhost:8004/docs
- **Support Service**: http://localhost:8005/docs
- **Themes Service**: http://localhost:8006/docs
- **Notifications Service**: http://localhost:8007/docs
- **Workers Service**: http://localhost:8008/docs

### Monitoring

- **Grafana**: http://localhost:3002 (admin/admin)
- **Prometheus**: http://localhost:9090
- **MinIO Console**: http://localhost:9001 (vetrai_minio_access/vetrai_minio_secret)

## First Steps

### 1. Log In as Admin

Use the default admin credentials (or the ones you set in `.env`):

```bash
curl -X POST http://localhost:8001/api/v1/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@vetrai.io",
    "password": "Admin@123"
  }'
```

Response:
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "email": "admin@vetrai.io",
    "role": "super_admin",
    ...
  }
}
```

Save the `access_token` for subsequent requests.

### 2. Create Your First Organization

```bash
curl -X POST http://localhost:8002/api/v1/organizations \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "name": "My Organization",
    "slug": "my-org",
    "plan": "pro",
    "max_users": 10,
    "max_api_keys": 20
  }'
```

### 3. Register a New User

```bash
curl -X POST http://localhost:8001/api/v1/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "SecurePass123!",
    "first_name": "John",
    "last_name": "Doe",
    "organization_id": 2,
    "role": "user"
  }'
```

### 4. Generate an API Key

```bash
curl -X POST http://localhost:8003/api/v1/keys \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "name": "My API Key",
    "scopes": ["read", "write"],
    "expires_at": "2025-12-31T23:59:59Z"
  }'
```

## Development Mode

### Running Services Locally

For development, you can run services locally without Docker:

```bash
# Navigate to a service directory
cd services/auth

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r ../shared/requirements.txt

# Run the service
uvicorn app.main:app --reload --port 8001
```

### Running Tests

```bash
# Install test dependencies
pip install pytest pytest-asyncio pytest-cov

# Run tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=services --cov-report=html
```

## Common Issues & Solutions

### Issue: Services won't start

**Solution:** Check Docker logs:
```bash
docker-compose logs [service-name]
```

### Issue: Database connection error

**Solution:** Ensure PostgreSQL is running and accessible:
```bash
docker-compose up -d postgres
docker-compose logs postgres
```

### Issue: Permission denied on scripts

**Solution:** Make scripts executable:
```bash
chmod +x scripts/setup/*.sh
chmod +x scripts/seeding/*.sh
```

### Issue: Port already in use

**Solution:** Change ports in `docker-compose.yml` or stop conflicting services:
```bash
# Find process using port 8001
lsof -i :8001
# Kill the process
kill -9 <PID>
```

## Next Steps

Now that you have VetrAI running, explore:

1. **[API Documentation](../api/README.md)** - Detailed API reference
2. **[Architecture Guide](../architecture/README.md)** - System design and patterns
3. **[Development Guide](development.md)** - Contributing and development workflow
4. **[Deployment Guide](../deployment/README.md)** - Production deployment

## Getting Help

- **Documentation**: Check `/docs` directory
- **GitHub Issues**: [Report bugs or request features](https://github.com/bininfotech0/vetrai_v5/issues)
- **Discord**: [Join our community](https://discord.gg/vetrai)
- **Email**: support@vetrai.io

## Stopping the Platform

To stop all services:

```bash
docker-compose down
```

To stop and remove all data (⚠️ destructive):

```bash
docker-compose down -v
```

---

**Happy building with VetrAI! 🚀**
