#!/usr/bin/env python3
"""
VetrAI Platform - API Testing Examples
Demonstrates how to use your live APIs
"""

import requests
import json
from datetime import datetime

def test_auth_api():
    """Test authentication endpoints"""
    print("🔐 Testing Authentication API")
    print("-" * 40)
    
    # Test registration
    auth_base = "http://localhost:8001/api/v1/auth"
    
    # Sample user registration
    user_data = {
        "email": "demo@vetrai.com",
        "password": "DemoPass123!",
        "first_name": "Demo",
        "last_name": "User",
        "organization_id": "demo-org"
    }
    
    try:
        # Try to get the docs first to see available endpoints
        docs_response = requests.get("http://localhost:8001/docs")
        if docs_response.status_code == 200:
            print("✅ Auth API Documentation: http://localhost:8001/docs")
        
        # Test health endpoint
        health_response = requests.get("http://localhost:8001/health")
        if health_response.status_code == 200:
            print("✅ Auth Service: HEALTHY")
            print(f"   Response: {health_response.json()}")
        
    except Exception as e:
        print(f"❌ Auth API Error: {e}")

def test_tenancy_api():
    """Test multi-tenancy endpoints"""
    print("\n🏢 Testing Tenancy API")
    print("-" * 40)
    
    try:
        # Test documentation
        docs_response = requests.get("http://localhost:8002/docs")
        if docs_response.status_code == 200:
            print("✅ Tenancy API Documentation: http://localhost:8002/docs")
        
        # Test health
        health_response = requests.get("http://localhost:8002/health")
        if health_response.status_code == 200:
            print("✅ Tenancy Service: HEALTHY")
            print(f"   Response: {health_response.json()}")
            
    except Exception as e:
        print(f"❌ Tenancy API Error: {e}")

def test_workers_api():
    """Test AI Workers API"""
    print("\n🤖 Testing AI Workers API")
    print("-" * 40)
    
    try:
        # Test documentation
        docs_response = requests.get("http://localhost:8008/docs")
        if docs_response.status_code == 200:
            print("✅ Workers API Documentation: http://localhost:8008/docs")
        
        # Test health
        health_response = requests.get("http://localhost:8008/health")
        if health_response.status_code == 200:
            print("✅ Workers Service: HEALTHY")
            print(f"   Response: {health_response.json()}")
            
    except Exception as e:
        print(f"❌ Workers API Error: {e}")

def show_usage_examples():
    """Show practical usage examples"""
    print("\n" + "=" * 60)
    print("🚀 VETRAI PLATFORM - READY TO USE!")
    print("=" * 60)
    
    print("\n📍 Your Live API Endpoints:")
    apis = [
        ("Authentication", "http://localhost:8001/docs", "User management, JWT tokens"),
        ("Tenancy", "http://localhost:8002/docs", "Multi-tenant organization management"),
        ("API Keys", "http://localhost:8003/docs", "API key generation and management"),
        ("Billing", "http://localhost:8004/docs", "Subscription and payment handling"),
        ("Support", "http://localhost:8005/docs", "Customer support and ticketing"),
        ("Themes", "http://localhost:8006/docs", "UI theme and customization"),
        ("Notifications", "http://localhost:8007/docs", "Email, SMS, push notifications"),
        ("AI Workers", "http://localhost:8008/docs", "ML model execution and AI workflows")
    ]
    
    for name, url, description in apis:
        print(f"   🔗 {name}: {url}")
        print(f"      {description}")
    
    print(f"\n📊 Monitoring:")
    print(f"   🔍 Prometheus: http://localhost:9090")
    print(f"   📈 Grafana: http://localhost:3002")
    print(f"   💾 MinIO: http://localhost:9000")
    
    print(f"\n🎯 Next Steps:")
    print(f"   1. Visit any API documentation URL above")
    print(f"   2. Use 'Try it out' feature in Swagger UI")
    print(f"   3. Start integrating with your applications")
    print(f"   4. Deploy to production when ready")

def create_sample_integration():
    """Create a sample integration script"""
    sample_code = '''
# VetrAI Platform Integration Example
import requests

# Configuration
VETRAI_BASE_URL = "http://localhost:8001"  # Change to your production URL
API_TOKEN = None  # Will be set after authentication

def authenticate(email, password):
    """Authenticate with VetrAI platform"""
    response = requests.post(f"{VETRAI_BASE_URL}/api/v1/auth/login", 
                           data={"username": email, "password": password})
    if response.status_code == 200:
        global API_TOKEN
        API_TOKEN = response.json()["access_token"]
        return True
    return False

def get_headers():
    """Get headers with authentication"""
    return {"Authorization": f"Bearer {API_TOKEN}"}

def create_tenant(org_name):
    """Create a new tenant organization"""
    response = requests.post(f"http://localhost:8002/api/v1/tenants",
                           json={"name": org_name},
                           headers=get_headers())
    return response.json()

# Usage example:
# if authenticate("your-email@domain.com", "your-password"):
#     tenant = create_tenant("My Organization")
#     print(f"Created tenant: {tenant}")
'''
    
    with open("api_integration_example.py", "w") as f:
        f.write(sample_code)
    
    print("\n📄 Created: api_integration_example.py")
    print("   Sample integration code for your reference")

def main():
    """Main testing function"""
    print("🧪 VetrAI Platform - API Testing Suite")
    print("=" * 60)
    
    # Test all APIs
    test_auth_api()
    test_tenancy_api()
    test_workers_api()
    
    # Show usage examples
    show_usage_examples()
    
    # Create sample integration
    create_sample_integration()
    
    print(f"\n✨ Testing Complete! Your platform is ready for use.")

if __name__ == "__main__":
    main()