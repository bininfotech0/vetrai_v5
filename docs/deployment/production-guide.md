# VetrAI Platform - Production Deployment Guide

## 🚀 Complete Production Deployment

This guide covers the complete deployment of the VetrAI platform for production environments.

## Prerequisites

### System Requirements
- **OS**: Linux/Windows with Docker support
- **RAM**: Minimum 8GB, Recommended 16GB
- **CPU**: Minimum 4 cores, Recommended 8 cores
- **Storage**: Minimum 50GB SSD space
- **Network**: Stable internet connection for container downloads

### Required Software
- Docker Engine 20.10+
- Docker Compose 2.0+
- Git
- Domain name and SSL certificate (for HTTPS)

## 🔧 Environment Configuration

### 1. Create Production Environment File
Create `.env.prod` with the following variables:

```bash
# Database Configuration
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
POSTGRES_DB=vetrai
POSTGRES_USER=vetrai
POSTGRES_PASSWORD=your_secure_postgres_password_here

# Redis Configuration
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_PASSWORD=your_secure_redis_password_here

# MinIO Configuration
MINIO_ACCESS_KEY=your_secure_minio_access_key_here
MINIO_SECRET_KEY=your_secure_minio_secret_key_here
MINIO_BUCKET=vetrai-storage

# JWT Configuration
JWT_SECRET_KEY=your_super_secret_jwt_key_minimum_32_characters_long
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=30

# Stripe Configuration (for payments)
STRIPE_PUBLIC_KEY=pk_live_your_stripe_public_key
STRIPE_SECRET_KEY=sk_live_your_stripe_secret_key
STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret

# Application Configuration
ENVIRONMENT=production
LOG_LEVEL=INFO
CORS_ORIGINS=["https://yourdomain.com","https://admin.yourdomain.com"]

# Email Configuration
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
FROM_EMAIL=noreply@yourdomain.com

# Frontend Configuration
REACT_APP_API_URL=https://api.yourdomain.com
NEXT_PUBLIC_API_URL=https://api.yourdomain.com
```

### 2. Generate Secure Secrets
```bash
# Generate JWT secret (Linux/Mac)
openssl rand -hex 32

# Generate passwords (Linux/Mac)
openssl rand -base64 32

# Windows PowerShell alternative
[System.Web.Security.Membership]::GeneratePassword(32, 4)
```

## 📦 Deployment Steps

### Step 1: Clone and Prepare Repository
```bash
# Clone repository
git clone https://github.com/your-org/vetrai_v5.git
cd vetrai_v5

# Copy production environment
cp .env.prod.example .env.prod
# Edit .env.prod with your actual values
```

### Step 2: Build Production Images
```bash
# Build all services for production
docker-compose -f docker-compose.yml -f docker-compose.prod.yml build

# Optional: Tag and push to registry
docker-compose -f docker-compose.yml -f docker-compose.prod.yml push
```

### Step 3: Initialize Database
```bash
# Start database first
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d postgres redis

# Wait for database to be ready
docker-compose -f docker-compose.yml -f docker-compose.prod.yml exec postgres pg_isready -U vetrai

# Run database migrations
docker-compose -f docker-compose.yml -f docker-compose.prod.yml exec auth-service alembic upgrade head
```

### Step 4: Deploy All Services
```bash
# Deploy entire platform
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d

# Monitor deployment
docker-compose -f docker-compose.yml -f docker-compose.prod.yml logs -f
```

### Step 5: Verify Deployment
```bash
# Check all services are healthy
docker-compose -f docker-compose.yml -f docker-compose.prod.yml ps

# Run health checks
curl http://localhost:8001/health  # Auth Service
curl http://localhost:8002/health  # Tenancy Service
curl http://localhost:3000         # Studio Frontend
curl http://localhost:3001         # Admin Dashboard
```

## 🔒 Security Configuration

### 1. SSL/TLS Setup (Reverse Proxy)
```nginx
# /etc/nginx/sites-available/vetrai.conf
server {
    listen 80;
    server_name yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com;
    
    ssl_certificate /path/to/your/certificate.crt;
    ssl_certificate_key /path/to/your/private.key;
    
    # Frontend - Studio
    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    # Backend API
    location /api/ {
        proxy_pass http://localhost:8001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

# Admin Dashboard
server {
    listen 443 ssl http2;
    server_name admin.yourdomain.com;
    
    ssl_certificate /path/to/your/certificate.crt;
    ssl_certificate_key /path/to/your/private.key;
    
    location / {
        proxy_pass http://localhost:3001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### 2. Firewall Configuration
```bash
# Ubuntu/Debian
sudo ufw allow 22        # SSH
sudo ufw allow 80        # HTTP
sudo ufw allow 443       # HTTPS
sudo ufw enable

# Close direct access to application ports
sudo ufw deny 3000
sudo ufw deny 3001
sudo ufw deny 8001-8008
```

### 3. Docker Security
```bash
# Create non-root user for Docker
sudo groupadd docker
sudo usermod -aG docker $USER

# Set Docker daemon security options in /etc/docker/daemon.json
{
  "live-restore": true,
  "userland-proxy": false,
  "icc": false,
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "100m",
    "max-file": "5"
  }
}

sudo systemctl reload docker
```

## 📊 Monitoring Setup

### 1. Access Monitoring Services
- **Prometheus**: http://localhost:9090
- **Grafana**: http://localhost:3000 (admin/admin123)

### 2. Configure Alerts
```bash
# Add alerting rules to prometheus.yml
# Configure Grafana dashboards for:
# - Service health monitoring
# - Resource utilization
# - Error rate tracking
# - Response time monitoring
```

### 3. Log Management
```bash
# Centralized logging with ELK Stack (optional)
docker-compose -f docker-compose.yml -f docker-compose.prod.yml -f docker-compose.logging.yml up -d
```

## 🔧 Maintenance

### Daily Operations
```bash
# Check service health
docker-compose -f docker-compose.yml -f docker-compose.prod.yml ps

# View logs
docker-compose -f docker-compose.yml -f docker-compose.prod.yml logs --tail=100 -f

# Update images (with downtime)
docker-compose -f docker-compose.yml -f docker-compose.prod.yml pull
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

### Database Backup
```bash
# Backup PostgreSQL
docker-compose -f docker-compose.yml -f docker-compose.prod.yml exec postgres pg_dump -U vetrai vetrai > backup_$(date +%Y%m%d_%H%M%S).sql

# Restore PostgreSQL
docker-compose -f docker-compose.yml -f docker-compose.prod.yml exec -T postgres psql -U vetrai vetrai < backup_file.sql
```

### Scaling Services
```bash
# Scale backend services
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d --scale workers-service=5 --scale auth-service=3

# Scale with Docker Swarm (advanced)
docker stack deploy -c docker-compose.yml -c docker-compose.prod.yml vetrai
```

## 🚨 Troubleshooting

### Common Issues

1. **Service Won't Start**
   ```bash
   # Check logs
   docker-compose -f docker-compose.yml -f docker-compose.prod.yml logs service-name
   
   # Check resource usage
   docker stats
   
   # Restart specific service
   docker-compose -f docker-compose.yml -f docker-compose.prod.yml restart service-name
   ```

2. **Database Connection Issues**
   ```bash
   # Check database status
   docker-compose -f docker-compose.yml -f docker-compose.prod.yml exec postgres pg_isready -U vetrai
   
   # Reset database (WARNING: Data loss)
   docker-compose -f docker-compose.yml -f docker-compose.prod.yml down -v
   docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
   ```

3. **Frontend Not Loading**
   ```bash
   # Check frontend build
   docker-compose -f docker-compose.yml -f docker-compose.prod.yml logs studio-frontend
   
   # Rebuild frontend
   docker-compose -f docker-compose.yml -f docker-compose.prod.yml build studio-frontend
   ```

### Performance Optimization

1. **Database Tuning**
   ```bash
   # PostgreSQL configuration in docker-compose.prod.yml
   command: postgres -c max_connections=200 -c shared_buffers=256MB -c effective_cache_size=1GB -c work_mem=4MB
   ```

2. **Redis Optimization**
   ```bash
   # Redis configuration
   command: redis-server --maxmemory 512mb --maxmemory-policy allkeys-lru
   ```

3. **Application Tuning**
   ```bash
   # Increase worker processes
   environment:
     WORKERS: 4
     WORKER_CONCURRENCY: 8
   ```

## 📈 Success Metrics

### Key Performance Indicators
- Service uptime > 99.9%
- API response time < 200ms (95th percentile)
- Database query time < 50ms (average)
- Error rate < 0.1%
- Memory usage < 80% of allocated
- CPU usage < 70% under normal load

### Monitoring Checklist
- [ ] All services responding to health checks
- [ ] Database connections within limits
- [ ] Redis memory usage optimized
- [ ] Frontend applications loading correctly
- [ ] API endpoints responding with correct schemas
- [ ] User authentication flows working
- [ ] File uploads/downloads functional
- [ ] Background job processing active

## 🎯 Next Steps

After successful deployment:

1. **Setup CI/CD Pipeline**
   - Automated testing on pull requests
   - Automated deployment on main branch
   - Blue-green deployment strategy

2. **Implement Monitoring Alerts**
   - Service down notifications
   - Performance threshold alerts
   - Error rate spike detection

3. **Setup Backup Strategy**
   - Automated daily database backups
   - File storage backups
   - Disaster recovery procedures

4. **Security Auditing**
   - Regular security updates
   - Penetration testing
   - Code security scanning

5. **Performance Optimization**
   - Load testing with realistic traffic
   - Database query optimization
   - CDN setup for static assets

---

## 📞 Support

For deployment support and troubleshooting:
- Documentation: `/docs`
- Health Checks: Run `python scripts/testing/e2e_testing.py`
- Logs: `docker-compose logs`
- Monitoring: Grafana dashboard

**VetrAI Platform is now ready for production! 🚀**