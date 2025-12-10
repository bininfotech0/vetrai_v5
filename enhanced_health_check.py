#!/usr/bin/env python3
"""
Enhanced Health Check Script
Provides detailed service health monitoring
"""

import requests
import json
import time
from datetime import datetime

def check_service_health():
    services = {
        "Auth": "http://localhost:8001/health",
        "Tenancy": "http://localhost:8002/health",
        "Keys": "http://localhost:8003/health",
        "Billing": "http://localhost:8004/health",
        "Support": "http://localhost:8005/health",
        "Themes": "http://localhost:8006/health",
        "Notifications": "http://localhost:8007/health",
        "Workers": "http://localhost:8008/health"
    }
    
    results = {}
    
    for name, url in services.items():
        try:
            start_time = time.time()
            response = requests.get(url, timeout=5)
            response_time = (time.time() - start_time) * 1000
            
            results[name] = {
                "status": "healthy" if response.status_code == 200 else "unhealthy",
                "response_code": response.status_code,
                "response_time_ms": round(response_time, 2),
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            results[name] = {
                "status": "error",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    return results

if __name__ == "__main__":
    health_data = check_service_health()
    
    print("VetrAI Platform Health Report")
    print("=" * 40)
    print(f"Timestamp: {datetime.now()}")
    print()
    
    for service, data in health_data.items():
        status_icon = "[OK]" if data.get("status") == "healthy" else "[ERR]"
        print(f"{status_icon} {service}: {data.get('status', 'unknown')}")
        
        if "response_time_ms" in data:
            print(f"   Response Time: {data['response_time_ms']}ms")
    
    # Save detailed report
    with open("health_report.json", "w") as f:
        json.dump(health_data, f, indent=2)
    
    print(f"\nDetailed report saved to: health_report.json")
