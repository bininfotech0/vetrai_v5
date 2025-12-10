# VetrAI Platform - Production Deployment Guide

This guide provides complete instructions for deploying the VetrAI platform to production with high availability, security, and monitoring.

## 🚀 Quick Start

### Option 1: Automated Deployment (Recommended)

```bash
# On your production server
curl -fsSL https://raw.githubusercontent.com/bininfotech0/vetrai_v5/main/scripts/setup/production_deploy.sh | sudo bash
```

### Option 2: Manual Deployment

```bash
# Clone repository
git clone https://github.com/bininfotech0/vetrai_v5.git /opt/vetrai
cd /opt/vetrai

# Run setup script
sudo chmod +x scripts/setup/production_deploy.sh
sudo ./scripts/setup/production_deploy.sh
```

## 📋 Prerequisites

### System Requirements
- **OS**: Ubuntu 20.04+ or Debian 11+ (recommended)
- **CPU**: 4+ cores (8+ cores recommended)
- **RAM**: 8GB minimum (16GB+ recommended)
- **Storage**: 100GB+ SSD
- **Network**: Static IP with domain names configured

### Domain Configuration
Configure the following DNS records:
```
vetrai.yourdomain.com       A    YOUR_SERVER_IP
admin.vetrai.yourdomain.com A    YOUR_SERVER_IP
api.vetrai.yourdomain.com   A    YOUR_SERVER_IP
```

## 🔧 Manual Installation Steps

### 1. System Preparation

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install -y curl wget git unzip software-properties-common

# Install Docker
curl -fsSL https://get.docker.com | sudo sh
sudo usermod -aG docker $USER

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.21.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

### 2. Project Setup

```bash
# Create project directory
sudo mkdir -p /opt/vetrai
sudo chown $USER:$USER /opt/vetrai

# Clone repository
git clone https://github.com/bininfotech0/vetrai_v5.git /opt/vetrai
cd /opt/vetrai
```

### 3. Environment Configuration

```bash
# Generate production environment file
cp .env.example .env.production

# Generate secure passwords
openssl rand -base64 32  # Use for POSTGRES_PASSWORD
openssl rand -base64 32  # Use for REDIS_PASSWORD
openssl rand -base64 64  # Use for JWT_SECRET_KEY
```

Edit `.env.production` with your configuration:
```bash
# Database Configuration
POSTGRES_PASSWORD=your_secure_postgres_password
REDIS_PASSWORD=your_secure_redis_password

# Security
JWT_SECRET_KEY=your_jwt_secret_key

# External Services
STRIPE_SECRET_KEY=your_stripe_key
OPENAI_API_KEY=your_openai_key

# Domains
DOMAIN=vetrai.yourdomain.com
ADMIN_DOMAIN=admin.vetrai.yourdomain.com
API_DOMAIN=api.vetrai.yourdomain.com
```

### 4. SSL Certificate Setup

```bash
# Option A: Let's Encrypt (Recommended)
sudo ./scripts/setup/ssl_setup.sh

# Option B: Custom certificates
# Place your certificates in:
# /etc/ssl/vetrai/vetrai.crt
# /etc/ssl/vetrai/vetrai.key
```

### 5. Deploy Services

```bash
# High Availability deployment
docker-compose -f docker-compose.ha.yml up -d

# Standard deployment
docker-compose -f docker-compose.prod.yml up -d
```

### 6. Verification

```bash
# Check service status
docker-compose -f docker-compose.ha.yml ps

# Run health checks
cd scripts/testing
python e2e_testing.py

# Test endpoints
curl -k https://vetrai.yourdomain.com/health
curl -k https://api.vetrai.yourdomain.com/health
```

## 🏗️ Architecture Overview

### High Availability Setup

```
Internet
    ↓
HAProxy Load Balancer (SSL Termination)
    ↓
Nginx Reverse Proxy (Primary + Secondary)
    ↓
Frontend Apps (Studio + Admin)
    ↓
Backend Services (8 Microservices)
    ↓
Database Layer (PostgreSQL + Redis + MinIO)
    ↓
Monitoring (Prometheus + Grafana)
```

### Service Distribution

| Component | Replicas | Resources | Ports |
|-----------|----------|-----------|-------|
| HAProxy | 1 | 0.5 CPU, 256MB | 80, 443, 8404 |
| Nginx | 2 | 0.5 CPU, 256MB | Internal |
| Frontend Services | 2-3 | 0.5 CPU, 512MB | Internal |
| Backend Services | 2-3 | 1 CPU, 1GB | Internal |
| PostgreSQL | 1+1 replica | 2 CPU, 2GB | 5432 |
| Redis | 1+1 replica | 0.5 CPU, 512MB | 6379 |
| MinIO | 1 | 0.5 CPU, 512MB | 9000 |

## 🔒 Security Configuration

### Firewall Setup
```bash
sudo ufw enable
sudo ufw allow 22/tcp   # SSH
sudo ufw allow 80/tcp   # HTTP
sudo ufw allow 443/tcp  # HTTPS
```

### SSL/TLS Configuration
- TLS 1.2+ only
- Modern cipher suites
- HSTS headers
- Security headers (X-Frame-Options, X-Content-Type-Options, etc.)

### Application Security
- JWT token authentication
- Password hashing with bcrypt
- SQL injection protection
- CORS configuration
- Rate limiting
- Input validation

## 📊 Monitoring & Logging

### Access URLs
- **HAProxy Stats**: http://your-server:8404/stats
- **Prometheus**: http://your-server:9090
- **Grafana**: http://your-server:3000

### Default Credentials
- **Grafana**: admin / (check .env.production for GRAFANA_PASSWORD)
- **HAProxy Stats**: admin / (check .env.production for HAPROXY_STATS_PASSWORD)

### Key Metrics to Monitor
- Service health and uptime
- Response times and latency
- Database performance
- Resource utilization (CPU, Memory, Disk)
- Error rates and status codes

## 🔄 Backup & Recovery

### Automated Backups
```bash
# Backup script is automatically created at:
/opt/vetrai/scripts/backup.sh

# Manual backup
sudo /opt/vetrai/scripts/backup.sh

# Backups are stored in:
/opt/vetrai/backups/
```

### Recovery Process
```bash
# Stop services
docker-compose -f docker-compose.ha.yml down

# Restore database
gunzip < backup_file.sql.gz | docker exec -i postgres psql -U vetrai

# Restore files
tar -xzf config_backup.tar.gz
tar -xzf minio_backup.tar.gz

# Restart services
docker-compose -f docker-compose.ha.yml up -d
```

## 🚀 Scaling & Performance

### Horizontal Scaling
```bash
# Scale specific services
docker-compose -f docker-compose.ha.yml up -d --scale workers-service=5
docker-compose -f docker-compose.ha.yml up -d --scale auth-service=3
```

### Performance Optimization
- Redis caching for frequently accessed data
- Database connection pooling
- CDN for static assets
- Image optimization
- Gzip compression

## 🔧 Maintenance

### Regular Updates
```bash
cd /opt/vetrai
git pull origin main
docker-compose -f docker-compose.ha.yml build --no-cache
docker-compose -f docker-compose.ha.yml up -d
```

### Log Management
```bash
# View logs
docker-compose -f docker-compose.ha.yml logs -f [service_name]

# Log rotation is automatically configured
# Logs are kept for 30 days
```

### Database Maintenance
```bash
# Database stats
docker-compose -f docker-compose.ha.yml exec postgres psql -U vetrai -c "SELECT * FROM pg_stat_database;"

# Vacuum and analyze
docker-compose -f docker-compose.ha.yml exec postgres psql -U vetrai -c "VACUUM ANALYZE;"
```

## 🚨 Troubleshooting

### Common Issues

**Services not starting**
```bash
# Check logs
docker-compose -f docker-compose.ha.yml logs [service_name]

# Check system resources
htop
df -h
```

**Database connection issues**
```bash
# Check database status
docker-compose -f docker-compose.ha.yml exec postgres pg_isready

# Check connectivity
docker-compose -f docker-compose.ha.yml exec auth-service nc -zv postgres 5432
```

**SSL/Certificate issues**
```bash
# Check certificate validity
openssl x509 -in /etc/ssl/vetrai/vetrai.crt -text -noout

# Test SSL
curl -vI https://vetrai.yourdomain.com
```

### Health Check Commands
```bash
# Overall system health
cd /opt/vetrai/scripts/testing
python production_optimization.py

# Service-specific health
curl -f http://localhost:8404/stats  # HAProxy
curl -f http://localhost:9090/-/healthy  # Prometheus
curl -f http://localhost:3000/api/health  # Grafana
```

## 📞 Support

For issues and support:
1. Check logs: `docker-compose logs -f`
2. Review health checks: `python scripts/testing/e2e_testing.py`
3. Monitor metrics: Access Grafana dashboards
4. Create GitHub issue with logs and error details

## 📚 Additional Resources

- [API Documentation](docs/api/README.md)
- [Architecture Guide](docs/architecture/README.md)
- [Security Guide](SECURITY.md)
- [Contributing Guide](CONTRIBUTING.md)

---

**🎉 Your VetrAI platform is now ready for production! 🚀**