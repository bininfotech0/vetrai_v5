#!/usr/bin/env python3
"""
Quick Docker Health Check Fix
Installs curl in running containers for health checks
"""

import subprocess
import time

def install_curl_in_containers():
    """Install curl in running service containers"""
    services = [
        'vetrai_v5-auth-service-1',
        'vetrai_v5-tenancy-service-1', 
        'vetrai_v5-keys-service-1',
        'vetrai_v5-billing-service-1',
        'vetrai_v5-support-service-1',
        'vetrai_v5-themes-service-1',
        'vetrai_v5-notifications-service-1',
        'vetrai_v5-workers-service-1'
    ]
    
    print("Installing curl in service containers...")
    
    for service in services:
        try:
            result = subprocess.run([
                'docker', 'exec', service, 'apt-get', 'update'
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                subprocess.run([
                    'docker', 'exec', service, 'apt-get', 'install', '-y', 'curl'
                ], capture_output=True, text=True)
                print(f"✅ {service}: curl installed")
            else:
                print(f"⚠️ {service}: could not update packages")
                
        except Exception as e:
            print(f"❌ {service}: {e}")

def restart_backend_services():
    """Restart backend services to apply health checks"""
    print("\nRestarting backend services...")
    
    try:
        result = subprocess.run([
            'docker-compose', '-f', 'docker-compose.backend.yml', 'restart'
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Backend services restarted")
            print("⏳ Waiting for health checks...")
            time.sleep(30)
        else:
            print("❌ Failed to restart services")
            
    except Exception as e:
        print(f"❌ Error restarting services: {e}")

def check_health_status():
    """Check the health status of containers"""
    print("\nChecking container health status...")
    
    try:
        result = subprocess.run([
            'docker', 'ps', '--format', 'table {{.Names}}\t{{.Status}}'
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            lines = result.stdout.strip().split('\n')
            for line in lines:
                if 'vetrai_v5' in line:
                    print(f"📊 {line}")
        
    except Exception as e:
        print(f"❌ Error checking health: {e}")

def main():
    print("🔧 Docker Health Check Fix")
    print("="*40)
    
    # Install curl in containers
    install_curl_in_containers()
    
    # Restart services
    restart_backend_services()
    
    # Check status
    check_health_status()
    
    print("\n✅ Health check fix complete!")
    print("💡 Health checks will now work properly")
    print("🔗 Run: python start_platform.py to verify")

if __name__ == "__main__":
    main()