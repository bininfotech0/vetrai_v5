#!/bin/bash
# VetrAI Platform - Production Deployment Helper
# Simple script to guide production deployment

echo "VetrAI Platform Production Deployment"
echo "====================================="

echo "Checking prerequisites..."

# Check Docker
if ! command -v docker &> /dev/null; then
    echo "ERROR: Docker is required. Please install Docker first."
    exit 1
fi

echo "Prerequisites check passed"

echo ""
echo "Choose deployment method:"
echo "1. Local production deployment"
echo "2. Cloud provider deployment"  
echo "3. Development environment info"

read -p "Enter your choice (1-3): " choice

case $choice in
    1)
        echo "Setting up local production environment..."
        echo "1. Copy .env.example to .env.production"
        echo "2. Edit .env.production with your settings"
        echo "3. Run: docker-compose -f docker-compose.ha.yml up -d"
        ;;
    2)
        echo "Cloud deployment options:"
        echo "• AWS: Upload project to EC2 or use ECS"
        echo "• Azure: Use Container Apps"
        echo "• GCP: Use Cloud Run"
        echo "• DigitalOcean: Use App Platform"
        echo ""
        echo "Use the scripts in /scripts/setup/ for automated deployment"
        ;;
    3)
        echo "Development environment info:"
        echo "Your platform is already running!"
        echo "• Studio: http://localhost:3000"
        echo "• Admin: http://localhost:3001"
        echo "• APIs: http://localhost:8001-8008/docs"
        ;;
    *)
        echo "Invalid choice. Please run the script again."
        ;;
esac

echo ""
echo "VetrAI Platform deployment helper complete!"
echo "Check NEXT_STEPS.md for detailed guidance"