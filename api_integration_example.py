
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
