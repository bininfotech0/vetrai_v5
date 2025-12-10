"""
Quick API Test - Use this to verify your platform
"""
import requests

# Test a simple API call
try:
    response = requests.get("http://localhost:8001/health")
    print(f"✅ Platform Status: {response.json()}")
    
    # Test Auth API documentation
    docs = requests.get("http://localhost:8001/docs")
    print(f"✅ Auth API Docs: Available ({docs.status_code})")
    
    print("\n🎯 Your platform is ready!")
    print("Next: Visit http://localhost:8001/docs in your browser")
    
except Exception as e:
    print(f"❌ Error: {e}")