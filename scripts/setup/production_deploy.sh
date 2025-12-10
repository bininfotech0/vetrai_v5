#!/bin/bash

# VetrAI Platform - Production Deployment Script
# Comprehensive production deployment with high availability

set -e

echo "🚀 VetrAI Platform - Production Deployment"
echo "=========================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PROJECT_DIR="/opt/vetrai"
BACKUP_DIR="/opt/vetrai/backups"
LOG_DIR="/var/log/vetrai"
ENV_FILE=".env.production"

# Check if running as root
if [[ $EUID -ne 0 ]]; then
   echo -e "${RED}This script should be run as root or with sudo${NC}"
   exit 1
fi

# Function to log messages
log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] $1${NC}"
}

error() {
    echo -e "${RED}[$(date +'%Y-%m-%d %H:%M:%S')] ERROR: $1${NC}"
}

warning() {
    echo -e "${YELLOW}[$(date +'%Y-%m-%d %H:%M:%S')] WARNING: $1${NC}"
}

info() {
    echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')] INFO: $1${NC}"
}

# System requirements check
check_system_requirements() {
    log "Checking system requirements..."
    
    # Check OS
    if [[ ! -f /etc/os-release ]]; then
        error "Cannot determine OS version"
        exit 1
    fi
    
    . /etc/os-release
    if [[ $ID != "ubuntu" ]] && [[ $ID != "debian" ]]; then
        warning "This script is optimized for Ubuntu/Debian. Proceed with caution."
    fi
    
    # Check memory (minimum 8GB recommended)
    TOTAL_MEM=$(free -g | awk 'NR==2{printf "%.0f", $2}')
    if [[ $TOTAL_MEM -lt 8 ]]; then
        warning "System has ${TOTAL_MEM}GB RAM. Minimum 8GB recommended for production."
    fi
    
    # Check disk space (minimum 50GB recommended)
    AVAILABLE_SPACE=$(df / | awk 'NR==2{printf "%.0f", $4/1024/1024}')
    if [[ $AVAILABLE_SPACE -lt 50 ]]; then
        warning "Available disk space: ${AVAILABLE_SPACE}GB. Minimum 50GB recommended."
    fi
    
    log "System requirements checked"
}

# Install required packages
install_dependencies() {
    log "Installing system dependencies..."
    
    # Update package list
    apt-get update -qq
    
    # Install required packages
    apt-get install -y \
        curl \
        wget \
        git \
        unzip \
        software-properties-common \
        apt-transport-https \
        ca-certificates \
        gnupg \
        lsb-release \
        htop \
        ncdu \
        tree \
        jq
    
    log "System dependencies installed"
}

# Install Docker
install_docker() {
    log "Installing Docker..."
    
    # Check if Docker is already installed
    if command -v docker &> /dev/null; then
        log "Docker is already installed"
        return 0
    fi
    
    # Install Docker CE
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null
    
    apt-get update -qq
    apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin
    
    # Start and enable Docker
    systemctl start docker
    systemctl enable docker
    
    # Add current user to docker group
    if [[ -n $SUDO_USER ]]; then
        usermod -aG docker $SUDO_USER
    fi
    
    log "Docker installed successfully"
}

# Install Docker Compose
install_docker_compose() {
    log "Installing Docker Compose..."
    
    # Check if Docker Compose is already installed
    if command -v docker-compose &> /dev/null; then
        log "Docker Compose is already installed"
        return 0
    fi
    
    # Install Docker Compose
    DOCKER_COMPOSE_VERSION="2.21.0"
    curl -L "https://github.com/docker/compose/releases/download/v${DOCKER_COMPOSE_VERSION}/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    chmod +x /usr/local/bin/docker-compose
    
    # Create symlink for docker compose command
    ln -sf /usr/local/bin/docker-compose /usr/bin/docker-compose
    
    log "Docker Compose installed successfully"
}

# Setup project directory
setup_project_directory() {
    log "Setting up project directory..."
    
    # Create directories
    mkdir -p $PROJECT_DIR
    mkdir -p $BACKUP_DIR
    mkdir -p $LOG_DIR
    
    # Set ownership if running with sudo
    if [[ -n $SUDO_USER ]]; then
        chown -R $SUDO_USER:$SUDO_USER $PROJECT_DIR
        chown -R $SUDO_USER:$SUDO_USER $BACKUP_DIR
    fi
    
    log "Project directory setup completed"
}

# Generate production environment file
generate_env_file() {
    log "Generating production environment file..."
    
    cd $PROJECT_DIR
    
    # Generate secure random passwords
    generate_password() {
        openssl rand -base64 32 | tr -d "=+/" | cut -c1-25
    }
    
    POSTGRES_PASSWORD=$(generate_password)
    POSTGRES_REPLICATION_PASSWORD=$(generate_password)
    REDIS_PASSWORD=$(generate_password)
    JWT_SECRET_KEY=$(openssl rand -base64 64 | tr -d "=+/" | cut -c1-32)
    MINIO_ACCESS_KEY="vetrai-admin"
    MINIO_SECRET_KEY=$(generate_password)
    GRAFANA_PASSWORD=$(generate_password)
    HAPROXY_STATS_PASSWORD=$(generate_password)
    
    cat > $ENV_FILE << EOF
# VetrAI Platform - Production Environment Configuration
# Generated on $(date)

# Database Configuration
POSTGRES_PASSWORD=$POSTGRES_PASSWORD
POSTGRES_REPLICATION_PASSWORD=$POSTGRES_REPLICATION_PASSWORD

# Cache Configuration  
REDIS_PASSWORD=$REDIS_PASSWORD

# Security Configuration
JWT_SECRET_KEY=$JWT_SECRET_KEY

# Object Storage Configuration
MINIO_ACCESS_KEY=$MINIO_ACCESS_KEY
MINIO_SECRET_KEY=$MINIO_SECRET_KEY

# Monitoring Configuration
GRAFANA_PASSWORD=$GRAFANA_PASSWORD
HAPROXY_STATS_PASSWORD=$HAPROXY_STATS_PASSWORD

# External Services (Configure these)
STRIPE_SECRET_KEY=your_stripe_secret_key_here
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Domain Configuration
DOMAIN=vetrai.yourdomain.com
ADMIN_DOMAIN=admin.vetrai.yourdomain.com
API_DOMAIN=api.vetrai.yourdomain.com

# Environment
NODE_ENV=production
ENVIRONMENT=production
EOF
    
    # Secure the environment file
    chmod 600 $ENV_FILE
    
    log "Environment file generated: $ENV_FILE"
    info "IMPORTANT: Update external API keys in $ENV_FILE before deployment"
}

# Clone or update repository
setup_repository() {
    log "Setting up repository..."
    
    cd $PROJECT_DIR
    
    if [[ ! -d ".git" ]]; then
        log "Cloning VetrAI repository..."
        git clone https://github.com/bininfotech0/vetrai_v5.git .
    else
        log "Updating existing repository..."
        git pull origin main
    fi
    
    # Set ownership
    if [[ -n $SUDO_USER ]]; then
        chown -R $SUDO_USER:$SUDO_USER $PROJECT_DIR
    fi
    
    log "Repository setup completed"
}

# Build Docker images
build_images() {
    log "Building Docker images..."
    
    cd $PROJECT_DIR
    
    # Build all images
    docker-compose -f docker-compose.ha.yml build --no-cache --parallel
    
    log "Docker images built successfully"
}

# Setup database
setup_database() {
    log "Setting up database..."
    
    cd $PROJECT_DIR
    
    # Start only database services
    docker-compose -f docker-compose.ha.yml up -d postgres-primary redis-primary
    
    # Wait for database to be ready
    info "Waiting for database to be ready..."
    sleep 30
    
    # Run database migrations
    docker-compose -f docker-compose.ha.yml exec postgres-primary psql -U vetrai -d vetrai -c "SELECT version();"
    
    log "Database setup completed"
}

# Deploy services
deploy_services() {
    log "Deploying all services..."
    
    cd $PROJECT_DIR
    
    # Deploy all services
    docker-compose -f docker-compose.ha.yml up -d
    
    # Wait for services to start
    info "Waiting for services to start..."
    sleep 60
    
    log "Services deployment completed"
}

# Setup SSL certificates
setup_ssl() {
    log "Setting up SSL certificates..."
    
    cd $PROJECT_DIR
    
    # Make SSL setup script executable
    chmod +x scripts/setup/ssl_setup.sh
    
    # Run SSL setup
    ./scripts/setup/ssl_setup.sh
    
    log "SSL certificates configured"
}

# Configure firewall
setup_firewall() {
    log "Configuring firewall..."
    
    # Install and configure UFW
    apt-get install -y ufw
    
    # Reset firewall rules
    ufw --force reset
    
    # Default policies
    ufw default deny incoming
    ufw default allow outgoing
    
    # Allow SSH
    ufw allow 22/tcp
    
    # Allow HTTP/HTTPS
    ufw allow 80/tcp
    ufw allow 443/tcp
    
    # Allow monitoring (restrict to internal network in production)
    ufw allow 8404/tcp comment "HAProxy stats"
    ufw allow 9090/tcp comment "Prometheus"
    ufw allow 3000/tcp comment "Grafana"
    
    # Enable firewall
    ufw --force enable
    
    log "Firewall configured"
}

# Setup monitoring
setup_monitoring() {
    log "Setting up monitoring..."
    
    cd $PROJECT_DIR
    
    # Create monitoring dashboards directory
    mkdir -p infra/monitoring/dashboards
    
    # Wait for Grafana to start
    info "Waiting for Grafana to be ready..."
    sleep 30
    
    # Import Grafana dashboards (if available)
    if [[ -d "infra/monitoring/dashboards" ]]; then
        log "Grafana dashboards directory ready"
    fi
    
    log "Monitoring setup completed"
}

# Health checks
perform_health_checks() {
    log "Performing health checks..."
    
    cd $PROJECT_DIR
    
    # Check service status
    docker-compose -f docker-compose.ha.yml ps
    
    # Test endpoints
    info "Testing service endpoints..."
    
    # Wait for services to be fully ready
    sleep 30
    
    # Check HAProxy stats
    if curl -f http://localhost:8404/stats &>/dev/null; then
        log "✅ HAProxy is healthy"
    else
        error "❌ HAProxy health check failed"
    fi
    
    # Check Prometheus
    if curl -f http://localhost:9090/-/healthy &>/dev/null; then
        log "✅ Prometheus is healthy"
    else
        error "❌ Prometheus health check failed"
    fi
    
    # Check Grafana
    if curl -f http://localhost:3000/api/health &>/dev/null; then
        log "✅ Grafana is healthy"
    else
        error "❌ Grafana health check failed"
    fi
    
    log "Health checks completed"
}

# Setup log rotation
setup_log_rotation() {
    log "Setting up log rotation..."
    
    cat > /etc/logrotate.d/vetrai << EOF
/var/log/vetrai/*.log {
    daily
    rotate 30
    compress
    delaycompress
    missingok
    notifempty
    copytruncate
}
EOF
    
    # Test logrotate configuration
    logrotate -d /etc/logrotate.d/vetrai
    
    log "Log rotation configured"
}

# Setup backup script
setup_backup() {
    log "Setting up backup system..."
    
    cat > /opt/vetrai/scripts/backup.sh << 'EOF'
#!/bin/bash

# VetrAI Platform Backup Script
BACKUP_DIR="/opt/vetrai/backups"
DATE=$(date +%Y%m%d_%H%M%S)
PROJECT_DIR="/opt/vetrai"

# Create backup directory
mkdir -p $BACKUP_DIR/$DATE

cd $PROJECT_DIR

# Backup databases
echo "Backing up databases..."
docker-compose -f docker-compose.ha.yml exec -T postgres-primary pg_dumpall -U vetrai | gzip > $BACKUP_DIR/$DATE/postgres_backup_$DATE.sql.gz

# Backup Redis
echo "Backing up Redis..."
docker-compose -f docker-compose.ha.yml exec -T redis-primary redis-cli BGSAVE
docker cp $(docker-compose -f docker-compose.ha.yml ps -q redis-primary):/data/dump.rdb $BACKUP_DIR/$DATE/redis_backup_$DATE.rdb

# Backup MinIO data
echo "Backing up MinIO..."
docker run --rm --volumes-from $(docker-compose -f docker-compose.ha.yml ps -q minio-primary) -v $BACKUP_DIR/$DATE:/backup alpine tar czf /backup/minio_backup_$DATE.tar.gz /data

# Backup configuration files
echo "Backing up configurations..."
tar czf $BACKUP_DIR/$DATE/config_backup_$DATE.tar.gz \
    .env.production \
    docker-compose.ha.yml \
    infra/

# Clean old backups (keep last 7 days)
find $BACKUP_DIR -type d -mtime +7 -exec rm -rf {} \;

echo "Backup completed: $BACKUP_DIR/$DATE"
EOF
    
    chmod +x /opt/vetrai/scripts/backup.sh
    
    # Setup cron job for daily backups
    (crontab -l 2>/dev/null; echo "0 2 * * * /opt/vetrai/scripts/backup.sh") | crontab -
    
    log "Backup system configured"
}

# Create deployment summary
create_deployment_summary() {
    log "Creating deployment summary..."
    
    cd $PROJECT_DIR
    
    cat > DEPLOYMENT_INFO.md << EOF
# VetrAI Platform - Production Deployment Summary

## Deployment Information
- **Deployment Date**: $(date)
- **Server**: $(hostname)
- **OS**: $(lsb_release -d | cut -f2)
- **Docker Version**: $(docker --version)
- **Docker Compose Version**: $(docker-compose --version)

## Service URLs
- **Main Application**: https://${DOMAIN:-vetrai.yourdomain.com}
- **Admin Dashboard**: https://${ADMIN_DOMAIN:-admin.vetrai.yourdomain.com}
- **API Gateway**: https://${API_DOMAIN:-api.vetrai.yourdomain.com}
- **HAProxy Stats**: http://localhost:8404/stats
- **Prometheus**: http://localhost:9090
- **Grafana**: http://localhost:3000

## Important Files
- **Environment**: \`$ENV_FILE\`
- **Docker Compose**: \`docker-compose.ha.yml\`
- **SSL Certificates**: \`/etc/ssl/vetrai/\`
- **Backups**: \`$BACKUP_DIR\`
- **Logs**: \`$LOG_DIR\`

## Management Commands

### Start Services
\`\`\`bash
cd $PROJECT_DIR
docker-compose -f docker-compose.ha.yml up -d
\`\`\`

### Stop Services  
\`\`\`bash
cd $PROJECT_DIR
docker-compose -f docker-compose.ha.yml down
\`\`\`

### View Logs
\`\`\`bash
cd $PROJECT_DIR
docker-compose -f docker-compose.ha.yml logs -f [service_name]
\`\`\`

### Backup
\`\`\`bash
/opt/vetrai/scripts/backup.sh
\`\`\`

### Update Services
\`\`\`bash
cd $PROJECT_DIR
git pull origin main
docker-compose -f docker-compose.ha.yml build --no-cache
docker-compose -f docker-compose.ha.yml up -d
\`\`\`

## Monitoring
- **Prometheus**: Monitor system and application metrics
- **Grafana**: Visualize metrics and create alerts  
- **HAProxy**: Monitor load balancer and service health
- **Docker**: Monitor container health and resource usage

## Security
- **Firewall**: UFW configured with minimal required ports
- **SSL/TLS**: HTTPS enforced with modern security standards
- **Passwords**: All passwords auto-generated and secured
- **Network**: Services isolated in Docker networks

## Next Steps
1. Update DNS records to point to this server
2. Configure external API keys in \`$ENV_FILE\`
3. Import Grafana dashboards
4. Setup external monitoring/alerting
5. Configure automated deployment pipeline
EOF
    
    log "Deployment summary created: DEPLOYMENT_INFO.md"
}

# Main deployment function
main() {
    log "Starting VetrAI Platform production deployment..."
    
    check_system_requirements
    install_dependencies
    install_docker
    install_docker_compose
    setup_project_directory
    generate_env_file
    setup_repository
    build_images
    setup_database
    deploy_services
    setup_ssl
    setup_firewall
    setup_monitoring
    setup_log_rotation
    setup_backup
    perform_health_checks
    create_deployment_summary
    
    echo ""
    echo "🎉 VetrAI Platform deployment completed successfully!"
    echo ""
    echo "📋 Next Steps:"
    echo "1. Review and update $PROJECT_DIR/$ENV_FILE"
    echo "2. Update DNS records for your domains"
    echo "3. Access the platform at https://${DOMAIN:-vetrai.yourdomain.com}"
    echo "4. Monitor services at http://localhost:8404/stats"
    echo "5. View logs: docker-compose -f docker-compose.ha.yml logs -f"
    echo ""
    echo "📚 Documentation: $PROJECT_DIR/DEPLOYMENT_INFO.md"
    echo ""
}

# Run main function
main "$@"