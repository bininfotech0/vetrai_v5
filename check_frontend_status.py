#!/usr/bin/env python3
"""
VetrAI Platform Frontend Status Check
Validates that frontend applications are working correctly
"""

import requests
import time
import sys
from typing import Dict, List

def check_frontend_status():
    """Check the status of frontend applications"""
    
    print("🔍 VetrAI Platform Frontend Status Check")
    print("=" * 60)
    
    # Frontend endpoints to check
    endpoints = {
        "Studio Frontend": "http://localhost:3000",
        "Admin Dashboard": "http://localhost:3001",
    }
    
    # Backend API endpoints
    api_endpoints = {
        "Auth Service": "http://localhost:8001/health",
        "Tenancy Service": "http://localhost:8002/health", 
        "Keys Service": "http://localhost:8003/health",
        "Billing Service": "http://localhost:8004/health",
        "Support Service": "http://localhost:8005/health",
        "Themes Service": "http://localhost:8006/health",
        "Notifications Service": "http://localhost:8007/health",
        "Workers Service": "http://localhost:8008/health"
    }
    
    results = []
    
    # Check backend APIs first
    print("\n🔧 Backend API Services:")
    print("-" * 30)
    for service, url in api_endpoints.items():
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                print(f"✅ {service}: HEALTHY ({response.json().get('status', 'OK')})")
                results.append({"service": service, "status": "HEALTHY", "url": url})
            else:
                print(f"⚠️  {service}: HTTP {response.status_code}")
                results.append({"service": service, "status": "WARNING", "url": url})
        except requests.exceptions.RequestException as e:
            print(f"❌ {service}: CONNECTION FAILED")
            results.append({"service": service, "status": "FAILED", "url": url})
    
    # Check frontend applications
    print("\n🌐 Frontend Applications:")
    print("-" * 30)
    for service, url in endpoints.items():
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                if "Next.js" in response.text or "<!DOCTYPE html>" in response.text:
                    print(f"✅ {service}: ACCESSIBLE")
                    results.append({"service": service, "status": "ACCESSIBLE", "url": url})
                else:
                    print(f"⚠️  {service}: UNEXPECTED RESPONSE")
                    results.append({"service": service, "status": "WARNING", "url": url})
            else:
                print(f"❌ {service}: HTTP {response.status_code}")
                results.append({"service": service, "status": "FAILED", "url": url})
        except requests.exceptions.RequestException as e:
            print(f"❌ {service}: CONNECTION FAILED")
            results.append({"service": service, "status": "FAILED", "url": url})
    
    # Summary
    print("\n📊 Platform Status Summary:")
    print("-" * 40)
    
    healthy_count = len([r for r in results if r["status"] in ["HEALTHY", "ACCESSIBLE"]])
    total_count = len(results)
    
    if healthy_count == total_count:
        print("🟢 ALL SYSTEMS OPERATIONAL")
        print(f"   {healthy_count}/{total_count} services running correctly")
        print("\n🚀 Platform is ready for use:")
        print("   • Studio Frontend: http://localhost:3000")
        print("   • Admin Dashboard: http://localhost:3001")
        return True
    else:
        print(f"🟡 PARTIAL OPERATION")
        print(f"   {healthy_count}/{total_count} services healthy")
        
        failed_services = [r for r in results if r["status"] == "FAILED"]
        if failed_services:
            print("\n❌ Failed Services:")
            for service in failed_services:
                print(f"   • {service['service']}")
        return False

if __name__ == "__main__":
    success = check_frontend_status()
    sys.exit(0 if success else 1)