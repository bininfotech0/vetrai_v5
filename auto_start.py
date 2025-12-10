#!/usr/bin/env python3
"""
VetrAI Platform - Automated Startup
One-command platform startup with health verification
"""

import subprocess
import time
import requests

def main():
    print("Starting VetrAI Platform...")
    
    # Start backend services
    print("Starting backend services...")
    result = subprocess.run([
        'docker-compose', '-f', 'docker-compose.backend.yml', 'up', '-d'
    ], capture_output=True)
    
    if result.returncode == 0:
        print("[OK] Backend services started")
    else:
        print("[ERR] Failed to start backend services")
        return False
    
    # Wait for services to be ready
    print("Waiting for services to be ready...")
    time.sleep(30)
    
    # Verify services
    services = [8001, 8002, 8003, 8004, 8005, 8006, 8007, 8008]
    healthy_count = 0
    
    for port in services:
        try:
            response = requests.get(f"http://localhost:{port}/health", timeout=3)
            if response.status_code == 200:
                healthy_count += 1
        except:
            pass
    
    print(f"Health Check: {healthy_count}/{len(services)} services healthy")
    
    if healthy_count >= 6:
        print("[OK] Platform is ready!")
        print("Studio UI: http://localhost:3000")
        print("Admin Dashboard: http://localhost:3001")
        print("API Documentation: http://localhost:8008/docs")
        return True
    else:
        print("[WARN] Some services may need more time to start")
        return False

if __name__ == "__main__":
    main()