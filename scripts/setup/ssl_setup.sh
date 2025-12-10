#!/bin/bash

# VetrAI SSL/TLS Setup Script
# This script sets up SSL certificates for the VetrAI platform

set -e

echo "🔒 VetrAI Platform - SSL/TLS Setup"
echo "=================================="

# Configuration
DOMAIN="vetrai.yourdomain.com"
ADMIN_DOMAIN="admin.vetrai.yourdomain.com"
API_DOMAIN="api.vetrai.yourdomain.com"
EMAIL="admin@yourdomain.com"
CERT_DIR="/etc/ssl/vetrai"
NGINX_CONF_DIR="/etc/nginx/sites-available"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if running as root
if [[ $EUID -ne 0 ]]; then
   echo -e "${RED}This script must be run as root${NC}"
   exit 1
fi

echo "📋 Configuration:"
echo "   Primary Domain: $DOMAIN"
echo "   Admin Domain: $ADMIN_DOMAIN"
echo "   API Domain: $API_DOMAIN"
echo "   Email: $EMAIL"
echo ""

# Install required packages
echo "📦 Installing required packages..."
apt-get update -qq
apt-get install -y nginx certbot python3-certbot-nginx openssl

# Create certificate directory
echo "📁 Creating certificate directories..."
mkdir -p $CERT_DIR
mkdir -p $NGINX_CONF_DIR

# Method selection
echo ""
echo "🔐 SSL Certificate Setup Options:"
echo "1. Let's Encrypt (Recommended for production)"
echo "2. Self-signed certificates (Development/testing)"
echo ""
read -p "Choose option (1 or 2): " cert_option

case $cert_option in
    1)
        echo ""
        echo "🌐 Setting up Let's Encrypt certificates..."
        
        # Copy nginx configuration
        cp /app/infra/nginx/nginx.conf $NGINX_CONF_DIR/vetrai.conf
        
        # Update domains in nginx config
        sed -i "s/vetrai\.yourdomain\.com/$DOMAIN/g" $NGINX_CONF_DIR/vetrai.conf
        sed -i "s/admin\.vetrai\.yourdomain\.com/$ADMIN_DOMAIN/g" $NGINX_CONF_DIR/vetrai.conf
        sed -i "s/api\.vetrai\.yourdomain\.com/$API_DOMAIN/g" $NGINX_CONF_DIR/vetrai.conf
        
        # Enable site
        ln -sf $NGINX_CONF_DIR/vetrai.conf /etc/nginx/sites-enabled/
        rm -f /etc/nginx/sites-enabled/default
        
        # Test nginx configuration
        nginx -t
        
        # Start nginx
        systemctl start nginx
        systemctl enable nginx
        
        # Obtain Let's Encrypt certificates
        certbot --nginx -d $DOMAIN -d $ADMIN_DOMAIN -d $API_DOMAIN \
                --email $EMAIL --agree-tos --non-interactive \
                --redirect --expand
        
        # Setup auto-renewal
        echo "0 12 * * * /usr/bin/certbot renew --quiet" | crontab -
        
        echo -e "${GREEN}✅ Let's Encrypt certificates installed successfully!${NC}"
        ;;
        
    2)
        echo ""
        echo "🔒 Creating self-signed certificates..."
        
        # Create self-signed certificate
        openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
                -keyout $CERT_DIR/vetrai.key \
                -out $CERT_DIR/vetrai.crt \
                -subj "/C=US/ST=State/L=City/O=VetrAI/OU=IT/CN=$DOMAIN/emailAddress=$EMAIL" \
                -extensions v3_req \
                -config <(
cat <<EOF
[req]
distinguished_name = req_distinguished_name
req_extensions = v3_req
prompt = no

[req_distinguished_name]
C = US
ST = State
L = City
O = VetrAI
OU = IT Department
CN = $DOMAIN
emailAddress = $EMAIL

[v3_req]
keyUsage = keyEncipherment, dataEncipherment
extendedKeyUsage = serverAuth
subjectAltName = @alt_names

[alt_names]
DNS.1 = $DOMAIN
DNS.2 = $ADMIN_DOMAIN
DNS.3 = $API_DOMAIN
DNS.4 = localhost
EOF
)
        
        # Set permissions
        chmod 600 $CERT_DIR/vetrai.key
        chmod 644 $CERT_DIR/vetrai.crt
        
        # Copy and update nginx configuration for self-signed certs
        cp /app/infra/nginx/nginx.conf $NGINX_CONF_DIR/vetrai.conf
        sed -i "s|/etc/ssl/certs/vetrai.crt|$CERT_DIR/vetrai.crt|g" $NGINX_CONF_DIR/vetrai.conf
        sed -i "s|/etc/ssl/private/vetrai.key|$CERT_DIR/vetrai.key|g" $NGINX_CONF_DIR/vetrai.conf
        sed -i "s/vetrai\.yourdomain\.com/$DOMAIN/g" $NGINX_CONF_DIR/vetrai.conf
        sed -i "s/admin\.vetrai\.yourdomain\.com/$ADMIN_DOMAIN/g" $NGINX_CONF_DIR/vetrai.conf
        sed -i "s/api\.vetrai\.yourdomain\.com/$API_DOMAIN/g" $NGINX_CONF_DIR/vetrai.conf
        
        # Enable site
        ln -sf $NGINX_CONF_DIR/vetrai.conf /etc/nginx/sites-enabled/
        rm -f /etc/nginx/sites-enabled/default
        
        # Test and reload nginx
        nginx -t && systemctl reload nginx
        
        echo -e "${GREEN}✅ Self-signed certificates created successfully!${NC}"
        echo -e "${YELLOW}⚠️  Note: Browsers will show security warnings for self-signed certificates${NC}"
        ;;
        
    *)
        echo -e "${RED}Invalid option selected${NC}"
        exit 1
        ;;
esac

# Security hardening
echo ""
echo "🛡️  Applying security hardening..."

# Create DH parameters for stronger security
if [ ! -f /etc/ssl/certs/dhparam.pem ]; then
    echo "   Generating DH parameters (this may take a while)..."
    openssl dhparam -out /etc/ssl/certs/dhparam.pem 2048
fi

# Add DH parameters to nginx config if not already present
if ! grep -q "ssl_dhparam" $NGINX_CONF_DIR/vetrai.conf; then
    sed -i '/ssl_prefer_server_ciphers off;/a\    ssl_dhparam /etc/ssl/certs/dhparam.pem;' $NGINX_CONF_DIR/vetrai.conf
fi

# Configure firewall
echo "   Configuring firewall..."
ufw --force enable
ufw allow 22/tcp
ufw allow 80/tcp
ufw allow 443/tcp
ufw --force reload

# Test nginx configuration
nginx -t && systemctl reload nginx

echo ""
echo "🎉 SSL/TLS setup completed successfully!"
echo ""
echo "📋 Summary:"
echo "   ✅ SSL certificates configured"
echo "   ✅ Nginx reverse proxy configured"
echo "   ✅ Security headers enabled"
echo "   ✅ Rate limiting configured"
echo "   ✅ Firewall configured"
echo ""
echo "🌐 Access URLs:"
echo "   Main App: https://$DOMAIN"
echo "   Admin: https://$ADMIN_DOMAIN"
echo "   API: https://$API_DOMAIN"
echo ""
echo "🔧 Next steps:"
echo "   1. Update DNS records to point to this server"
echo "   2. Update frontend environment variables"
echo "   3. Test all endpoints"
echo "   4. Monitor logs: tail -f /var/log/nginx/access.log"