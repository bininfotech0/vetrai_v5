# VetrAI Platform - Deployment Guide

Complete guide for deploying VetrAI Platform to various environments.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Environment Configuration](#environment-configuration)
- [Docker Compose Deployment](#docker-compose-deployment)
- [Kubernetes Deployment](#kubernetes-deployment)
- [Database Setup](#database-setup)
- [SSL/TLS Configuration](#ssltls-configuration)
- [Monitoring Setup](#monitoring-setup)
- [Backup & Recovery](#backup--recovery)
- [Troubleshooting](#troubleshooting)

## Prerequisites

### Minimum Requirements

**Development**:
- 2 CPU cores
- 4 GB RAM
- 20 GB disk space

**Production**:
- 4 CPU cores
- 16 GB RAM
- 100 GB disk space (SSD recommended)

### Software Requirements

- Docker 20.10+
- Docker Compose 2.0+
- Kubernetes 1.24+ (for K8s deployment)
- Helm 3.0+ (for K8s deployment)
- PostgreSQL 15+ (if not using Docker)
- Redis 7+ (if not using Docker)

## Environment Configuration

### 1. Create Environment File

```bash
cp .env.example .env
```

### 2. Configure Essential Variables

Edit `.env` with production values:

```env
# Environment
ENVIRONMENT=production
DEBUG=false
LOG_LEVEL=INFO

# Security
SECRET_KEY=<generate-secure-random-key>
JWT_SECRET_KEY=<generate-secure-random-key>

# Database (use managed DB in production)
DATABASE_URL=postgresql://user:password@db-host:5432/vetrai_db
DATABASE_POOL_SIZE=20
DATABASE_MAX_OVERFLOW=10

# Redis (use managed Redis in production)
REDIS_URL=redis://redis-host:6379/0
REDIS_PASSWORD=<secure-password>

# MinIO/S3 (use AWS S3 or similar in production)
MINIO_ENDPOINT=s3.amazonaws.com
MINIO_ACCESS_KEY=<aws-access-key>
MINIO_SECRET_KEY=<aws-secret-key>
MINIO_SECURE=true
MINIO_BUCKET_NAME=vetrai-production

# SMTP
SMTP_HOST=smtp.sendgrid.net
SMTP_PORT=587
SMTP_USERNAME=apikey
SMTP_PASSWORD=<sendgrid-api-key>
SMTP_FROM_EMAIL=noreply@yourdomain.com

# Stripe
STRIPE_SECRET_KEY=sk_live_<your-stripe-secret>
STRIPE_PUBLISHABLE_KEY=pk_live_<your-stripe-publishable>
STRIPE_WEBHOOK_SECRET=whsec_<your-webhook-secret>

# CORS
CORS_ORIGINS=https://yourdomain.com,https://api.yourdomain.com

# SSL
SECURE_SSL_REDIRECT=true
SESSION_COOKIE_SECURE=true
CSRF_COOKIE_SECURE=true

# Admin
ADMIN_EMAIL=admin@yourdomain.com
ADMIN_PASSWORD=<secure-admin-password>
```

### 3. Generate Secure Keys

```bash
# Generate secret keys
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

## Docker Compose Deployment

### Development Environment

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Production Environment

1. **Create production compose file**:

```yaml
# docker-compose.prod.yml
version: '3.8'

services:
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./infra/nginx/nginx.conf:/etc/nginx/nginx.conf:ro
      - ./infra/nginx/ssl:/etc/nginx/ssl:ro
    depends_on:
      - auth-service
      - tenancy-service
    networks:
      - vetrai-network
    restart: always

  auth-service:
    build:
      context: ./services/auth
      dockerfile: Dockerfile
    environment:
      - ENVIRONMENT=production
      - DATABASE_URL=${DATABASE_URL}
      - REDIS_URL=${REDIS_URL}
    deploy:
      replicas: 3
      resources:
        limits:
          cpus: '1'
          memory: 1G
        reservations:
          cpus: '0.5'
          memory: 512M
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    networks:
      - vetrai-network
    restart: always

  # ... other services ...

networks:
  vetrai-network:
    driver: bridge

volumes:
  postgres_data:
  redis_data:
```

2. **Deploy to production**:

```bash
docker-compose -f docker-compose.prod.yml up -d
```

## Kubernetes Deployment

### 1. Install Helm Chart

```bash
# Add Helm repository
helm repo add vetrai https://charts.vetrai.io
helm repo update

# Create namespace
kubectl create namespace vetrai

# Install chart
helm install vetrai vetrai/vetrai-platform \
  --namespace vetrai \
  --values values-production.yaml
```

### 2. Production Values File

Create `values-production.yaml`:

```yaml
# Global configuration
global:
  domain: vetrai.io
  environment: production

# Ingress configuration
ingress:
  enabled: true
  className: nginx
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
  hosts:
    - host: api.vetrai.io
      paths:
        - path: /
          pathType: Prefix
  tls:
    - secretName: vetrai-tls
      hosts:
        - api.vetrai.io

# Auth Service
auth:
  replicaCount: 3
  image:
    repository: ghcr.io/bininfotech0/vetrai-auth
    tag: latest
  resources:
    limits:
      cpu: 1000m
      memory: 1Gi
    requests:
      cpu: 500m
      memory: 512Mi
  autoscaling:
    enabled: true
    minReplicas: 3
    maxReplicas: 10
    targetCPUUtilizationPercentage: 70

# PostgreSQL
postgresql:
  enabled: false  # Use managed database
  external:
    host: postgres.example.com
    port: 5432
    database: vetrai_db
    username: vetrai
    existingSecret: postgres-credentials

# Redis
redis:
  enabled: false  # Use managed Redis
  external:
    host: redis.example.com
    port: 6379
    existingSecret: redis-credentials

# MinIO (or use S3)
minio:
  enabled: false
  s3:
    bucket: vetrai-production
    region: us-east-1
    existingSecret: s3-credentials

# Monitoring
prometheus:
  enabled: true
  retention: 30d

grafana:
  enabled: true
  adminPassword: <secure-password>
```

### 3. Apply Secrets

```bash
# Database credentials
kubectl create secret generic postgres-credentials \
  --namespace vetrai \
  --from-literal=password=<db-password>

# Redis credentials
kubectl create secret generic redis-credentials \
  --namespace vetrai \
  --from-literal=password=<redis-password>

# S3 credentials
kubectl create secret generic s3-credentials \
  --namespace vetrai \
  --from-literal=access-key=<access-key> \
  --from-literal=secret-key=<secret-key>

# Stripe credentials
kubectl create secret generic stripe-credentials \
  --namespace vetrai \
  --from-literal=secret-key=<stripe-secret> \
  --from-literal=webhook-secret=<webhook-secret>
```

### 4. Verify Deployment

```bash
# Check pods
kubectl get pods -n vetrai

# Check services
kubectl get svc -n vetrai

# Check ingress
kubectl get ingress -n vetrai

# View logs
kubectl logs -f -n vetrai deployment/auth-service
```

## Database Setup

### PostgreSQL Configuration

1. **Create database and user**:

```sql
CREATE DATABASE vetrai_db;
CREATE USER vetrai WITH ENCRYPTED PASSWORD 'secure-password';
GRANT ALL PRIVILEGES ON DATABASE vetrai_db TO vetrai;

-- Enable extensions
\c vetrai_db
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";
CREATE EXTENSION IF NOT EXISTS "vector";
```

2. **Run migrations**:

```bash
./scripts/setup/migrate.sh
```

3. **Configure backups**:

```bash
# Daily backup script
0 2 * * * pg_dump vetrai_db | gzip > /backups/vetrai_$(date +\%Y\%m\%d).sql.gz
```

### Database Optimization

```sql
-- Analyze tables
ANALYZE;

-- Reindex if needed
REINDEX DATABASE vetrai_db;

-- Vacuum regularly
VACUUM ANALYZE;
```

## SSL/TLS Configuration

### Using Let's Encrypt

```bash
# Install certbot
sudo apt-get install certbot python3-certbot-nginx

# Obtain certificate
sudo certbot --nginx -d api.vetrai.io

# Auto-renewal
sudo certbot renew --dry-run
```

### Nginx Configuration

```nginx
server {
    listen 80;
    server_name api.vetrai.io;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name api.vetrai.io;

    ssl_certificate /etc/letsencrypt/live/api.vetrai.io/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/api.vetrai.io/privkey.pem;

    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    location / {
        proxy_pass http://auth-service:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## Monitoring Setup

### Prometheus Configuration

Already configured in `infra/monitoring/prometheus.yml`.

### Grafana Dashboards

1. **Access Grafana**: http://grafana.vetrai.io
2. **Import dashboards**:
   - VetrAI Overview
   - Service Metrics
   - Database Performance
   - API Analytics

### Alerting

Configure alerts in `infra/monitoring/alerts/`:

```yaml
groups:
  - name: vetrai_alerts
    interval: 30s
    rules:
      - alert: HighErrorRate
        expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.05
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: High error rate detected
```

## Backup & Recovery

### Automated Backups

```bash
# Database backup
pg_dump -h localhost -U vetrai vetrai_db | gzip > backup_$(date +%Y%m%d).sql.gz

# Upload to S3
aws s3 cp backup_$(date +%Y%m%d).sql.gz s3://vetrai-backups/

# Retain for 30 days
find /backups -name "backup_*.sql.gz" -mtime +30 -delete
```

### Recovery Procedure

```bash
# Download backup
aws s3 cp s3://vetrai-backups/backup_20240101.sql.gz .

# Restore database
gunzip < backup_20240101.sql.gz | psql -h localhost -U vetrai vetrai_db
```

## Troubleshooting

### Service Won't Start

```bash
# Check logs
docker-compose logs [service-name]
kubectl logs -n vetrai deployment/[service-name]

# Check resources
docker stats
kubectl top pods -n vetrai
```

### Database Connection Issues

```bash
# Test connection
psql -h db-host -U vetrai -d vetrai_db

# Check connection pool
docker-compose exec auth-service python -c "from shared.utils import engine; print(engine.pool.status())"
```

### High CPU/Memory Usage

```bash
# Identify bottleneck
kubectl top pods -n vetrai

# Scale up
kubectl scale deployment/auth-service --replicas=5 -n vetrai

# Check slow queries
SELECT * FROM pg_stat_statements ORDER BY total_time DESC LIMIT 10;
```

## Health Checks

Monitor service health:

```bash
# Check all services
for service in auth tenancy keys billing; do
  curl -f http://localhost:800${service#*}/health || echo "$service is down"
done
```

## Performance Tuning

### Database

```ini
# postgresql.conf
shared_buffers = 4GB
effective_cache_size = 12GB
maintenance_work_mem = 1GB
max_connections = 200
```

### Redis

```conf
# redis.conf
maxmemory 2gb
maxmemory-policy allkeys-lru
```

### Application

```env
# Increase worker processes
UVICORN_WORKERS=4

# Connection pooling
DATABASE_POOL_SIZE=20
DATABASE_MAX_OVERFLOW=10
```

---

For more deployment examples, see the [deployment examples](examples/) directory.
