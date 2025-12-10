#!/usr/bin/env python3
"""
VetrAI Backend Services Startup
Starts core services without problematic frontend builds
"""

import subprocess
import time
import sys
import os

def print_header(title):
    print(f"\n{'='*50}")
    print(f"🚀 {title}")
    print(f"{'='*50}")

def check_docker():
    """Check if Docker is running"""
    try:
        result = subprocess.run(['docker', 'info'], 
                              capture_output=True, text=True)
        return result.returncode == 0
    except:
        return False

def start_backend_services():
    """Start backend services only"""
    print_header("STARTING BACKEND SERVICES")
    
    backend_compose = """version: '3.8'

services:
  # Database Services
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: vetrai
      POSTGRES_USER: vetrai_user
      POSTGRES_PASSWORD: vetrai_pass
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  minio:
    image: minio/minio
    ports:
      - "9000:9000"
      - "9001:9001"
    environment:
      MINIO_ROOT_USER: minioadmin
      MINIO_ROOT_PASSWORD: minioadmin
    command: server /data --console-address ":9001"
    volumes:
      - minio_data:/data

  # Microservices
  auth-service:
    build: ./services/auth
    ports:
      - "8001:8001"
    environment:
      - DATABASE_URL=postgresql://vetrai_user:vetrai_pass@postgres:5432/vetrai
      - REDIS_URL=redis://redis:6379
    depends_on:
      - postgres
      - redis

  tenancy-service:
    build: ./services/tenancy
    ports:
      - "8002:8002"
    environment:
      - DATABASE_URL=postgresql://vetrai_user:vetrai_pass@postgres:5432/vetrai
      - REDIS_URL=redis://redis:6379
    depends_on:
      - postgres
      - redis

  keys-service:
    build: ./services/keys
    ports:
      - "8003:8003"
    environment:
      - DATABASE_URL=postgresql://vetrai_user:vetrai_pass@postgres:5432/vetrai
      - REDIS_URL=redis://redis:6379
    depends_on:
      - postgres
      - redis

  billing-service:
    build: ./services/billing
    ports:
      - "8004:8004"
    environment:
      - DATABASE_URL=postgresql://vetrai_user:vetrai_pass@postgres:5432/vetrai
      - REDIS_URL=redis://redis:6379
    depends_on:
      - postgres
      - redis

  support-service:
    build: ./services/support
    ports:
      - "8005:8005"
    environment:
      - DATABASE_URL=postgresql://vetrai_user:vetrai_pass@postgres:5432/vetrai
      - REDIS_URL=redis://redis:6379
    depends_on:
      - postgres
      - redis

  themes-service:
    build: ./services/themes
    ports:
      - "8006:8006"
    environment:
      - DATABASE_URL=postgresql://vetrai_user:vetrai_pass@postgres:5432/vetrai
      - REDIS_URL=redis://redis:6379
    depends_on:
      - postgres
      - redis

  notifications-service:
    build: ./services/notifications
    ports:
      - "8007:8007"
    environment:
      - DATABASE_URL=postgresql://vetrai_user:vetrai_pass@postgres:5432/vetrai
      - REDIS_URL=redis://redis:6379
    depends_on:
      - postgres
      - redis

  workers-service:
    build: ./services/workers
    ports:
      - "8008:8008"
    environment:
      - DATABASE_URL=postgresql://vetrai_user:vetrai_pass@postgres:5432/vetrai
      - REDIS_URL=redis://redis:6379
      - MINIO_URL=http://minio:9000
      - MINIO_ACCESS_KEY=minioadmin
      - MINIO_SECRET_KEY=minioadmin
    depends_on:
      - postgres
      - redis
      - minio

volumes:
  postgres_data:
  minio_data:
"""

    # Write backend-only compose file
    with open('docker-compose.backend.yml', 'w') as f:
        f.write(backend_compose)
    
    print("📝 Created docker-compose.backend.yml")
    
    try:
        print("🔧 Starting backend services...")
        result = subprocess.run([
            'docker-compose', '-f', 'docker-compose.backend.yml', 
            'up', '-d'
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Backend services started successfully!")
            return True
        else:
            print(f"❌ Error starting backend: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Failed to start backend services: {e}")
        return False

def wait_for_services():
    """Wait for services to be ready"""
    print("\n⏳ Waiting for services to be ready...")
    
    import requests
    services = [
        ("Auth", "http://localhost:8001/health"),
        ("Tenancy", "http://localhost:8002/health"),
        ("Keys", "http://localhost:8003/health"),
        ("Billing", "http://localhost:8004/health"),
        ("Support", "http://localhost:8005/health"),
        ("Themes", "http://localhost:8006/health"),
        ("Notifications", "http://localhost:8007/health"),
        ("Workers", "http://localhost:8008/health")
    ]
    
    max_wait = 120  # 2 minutes
    wait_time = 0
    
    while wait_time < max_wait:
        ready_count = 0
        for name, url in services:
            try:
                response = requests.get(url, timeout=2)
                if response.status_code == 200:
                    ready_count += 1
            except:
                pass
        
        if ready_count >= 6:  # At least 6 services ready
            print(f"✅ {ready_count}/8 services ready!")
            return True
        
        print(f"⏳ {ready_count}/8 services ready... waiting...")
        time.sleep(5)
        wait_time += 5
    
    print("⚠️ Some services may still be starting up")
    return False

def main():
    """Main function"""
    print_header("VETRAI BACKEND STARTUP")
    
    if not check_docker():
        print("❌ Docker is not running. Please start Docker and try again.")
        return False
    
    print("✅ Docker is running")
    
    # Start backend services
    if start_backend_services():
        print("\n🎉 Backend services starting...")
        
        # Wait for services
        if wait_for_services():
            print("\n✅ Platform ready!")
            print("\n🔗 Quick Links:")
            print("   📚 API Docs: http://localhost:8008/docs")
            print("   🤖 AI Endpoints: http://localhost:8008/ai/*")
            print("   📊 Database: localhost:5432")
            print("   💾 Redis: localhost:6379")
            print("   📁 MinIO: http://localhost:9000")
            
            print("\n🚀 Run this for complete status:")
            print("   python start_platform.py")
            
            return True
        else:
            print("\n⚠️ Some services may need more time to start")
            print("   Check status with: docker-compose -f docker-compose.backend.yml ps")
            return False
    else:
        print("\n❌ Failed to start backend services")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)