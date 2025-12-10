#!/usr/bin/env python3
"""
VetrAI Platform - API Integration Testing Suite
Tests all 8 microservices and their integration points
"""
import asyncio
import aiohttp
import json
import time
import sys
from typing import Dict, List, Any
from dataclasses import dataclass
from datetime import datetime

@dataclass
class TestResult:
    service: str
    endpoint: str
    method: str
    status_code: int
    response_time: float
    success: bool
    error_message: str = ""
    response_data: Any = None

class VetrAIAPITester:
    def __init__(self, base_url: str = "http://localhost"):
        self.base_url = base_url
        self.auth_token = None
        self.test_results: List[TestResult] = []
        
    async def run_all_tests(self):
        """Run comprehensive API integration tests"""
        print("🚀 Starting VetrAI Platform API Integration Tests")
        print("=" * 60)
        
        async with aiohttp.ClientSession() as session:
            # Test 1: Health checks for all services
            await self.test_health_checks(session)
            
            # Test 2: Authentication flow
            await self.test_authentication(session)
            
            # Test 3: Service integration tests
            if self.auth_token:
                await self.test_tenancy_service(session)
                await self.test_keys_service(session)
                await self.test_billing_service(session)
                await self.test_support_service(session)
                await self.test_themes_service(session)
                await self.test_notifications_service(session)
                await self.test_workers_service(session)
            
        self.print_test_summary()
    
    async def test_health_checks(self, session: aiohttp.ClientSession):
        """Test health endpoints for all services"""
        print("\n📊 Testing Health Endpoints...")
        
        services = [
            (8001, "auth"),
            (8002, "tenancy"), 
            (8003, "keys"),
            (8004, "billing"),
            (8005, "support"),
            (8006, "themes"),
            (8007, "notifications"),
            (8008, "workers")
        ]
        
        for port, service in services:
            await self.make_request(
                session, "GET", f"{self.base_url}:{port}/health",
                service, "/health"
            )
    
    async def test_authentication(self, session: aiohttp.ClientSession):
        """Test authentication service endpoints"""
        print("\n🔐 Testing Authentication Service...")
        
        # Test user registration
        register_data = {
            "email": "test@vetrai.io",
            "password": "TestPassword123!",
            "firstName": "Test",
            "lastName": "User",
            "organizationName": "Test Organization"
        }
        
        result = await self.make_request(
            session, "POST", f"{self.base_url}:8001/api/v1/auth/register",
            "auth", "/api/v1/auth/register", data=register_data
        )
        
        # If registration fails due to existing user, try login instead
        if result and not result.success and "already exists" in str(result.error_message):
            login_data = {
                "email": "test@vetrai.io",
                "password": "TestPassword123!"
            }
            
            result = await self.make_request(
                session, "POST", f"{self.base_url}:8001/api/v1/auth/login",
                "auth", "/api/v1/auth/login", data=login_data
            )
        
        # Extract auth token
        if result and result.success and result.response_data:
            if isinstance(result.response_data, dict):
                self.auth_token = result.response_data.get("access_token")
                print(f"✅ Authentication successful - Token acquired")
            else:
                print(f"❌ Authentication response format unexpected")
    
    async def test_tenancy_service(self, session: aiohttp.ClientSession):
        """Test tenancy service endpoints"""
        print("\n🏢 Testing Tenancy Service...")
        
        headers = {"Authorization": f"Bearer {self.auth_token}"}
        
        # Get organizations
        await self.make_request(
            session, "GET", f"{self.base_url}:8002/api/v1/tenancy/organizations",
            "tenancy", "/api/v1/tenancy/organizations", headers=headers
        )
    
    async def test_keys_service(self, session: aiohttp.ClientSession):
        """Test API keys service endpoints"""
        print("\n🔑 Testing Keys Service...")
        
        headers = {"Authorization": f"Bearer {self.auth_token}"}
        
        # List API keys
        await self.make_request(
            session, "GET", f"{self.base_url}:8003/api/v1/keys",
            "keys", "/api/v1/keys", headers=headers
        )
        
        # Create API key
        key_data = {
            "name": "Test API Key",
            "description": "Integration test key",
            "permissions": ["read", "write"]
        }
        
        await self.make_request(
            session, "POST", f"{self.base_url}:8003/api/v1/keys",
            "keys", "/api/v1/keys", headers=headers, data=key_data
        )
    
    async def test_billing_service(self, session: aiohttp.ClientSession):
        """Test billing service endpoints"""
        print("\n💳 Testing Billing Service...")
        
        headers = {"Authorization": f"Bearer {self.auth_token}"}
        
        # Get subscriptions
        await self.make_request(
            session, "GET", f"{self.base_url}:8004/api/v1/billing/subscriptions",
            "billing", "/api/v1/billing/subscriptions", headers=headers
        )
        
        # Get invoices
        await self.make_request(
            session, "GET", f"{self.base_url}:8004/api/v1/billing/invoices",
            "billing", "/api/v1/billing/invoices", headers=headers
        )
    
    async def test_support_service(self, session: aiohttp.ClientSession):
        """Test support service endpoints"""
        print("\n🎫 Testing Support Service...")
        
        headers = {"Authorization": f"Bearer {self.auth_token}"}
        
        # List tickets
        await self.make_request(
            session, "GET", f"{self.base_url}:8005/api/v1/support/tickets",
            "support", "/api/v1/support/tickets", headers=headers
        )
        
        # Create ticket
        ticket_data = {
            "title": "Integration Test Ticket",
            "description": "This is a test ticket created during integration testing",
            "priority": "medium"
        }
        
        await self.make_request(
            session, "POST", f"{self.base_url}:8005/api/v1/support/tickets",
            "support", "/api/v1/support/tickets", headers=headers, data=ticket_data
        )
    
    async def test_themes_service(self, session: aiohttp.ClientSession):
        """Test themes service endpoints"""
        print("\n🎨 Testing Themes Service...")
        
        headers = {"Authorization": f"Bearer {self.auth_token}"}
        
        # Get themes
        await self.make_request(
            session, "GET", f"{self.base_url}:8006/api/v1/themes",
            "themes", "/api/v1/themes", headers=headers
        )
    
    async def test_notifications_service(self, session: aiohttp.ClientSession):
        """Test notifications service endpoints"""
        print("\n📧 Testing Notifications Service...")
        
        headers = {"Authorization": f"Bearer {self.auth_token}"}
        
        # Get notifications
        await self.make_request(
            session, "GET", f"{self.base_url}:8007/api/v1/notifications",
            "notifications", "/api/v1/notifications", headers=headers
        )
        
        # Get templates
        await self.make_request(
            session, "GET", f"{self.base_url}:8007/api/v1/notifications/templates",
            "notifications", "/api/v1/notifications/templates", headers=headers
        )
    
    async def test_workers_service(self, session: aiohttp.ClientSession):
        """Test workers service endpoints"""
        print("\n⚙️ Testing Workers Service...")
        
        headers = {"Authorization": f"Bearer {self.auth_token}"}
        
        # Get jobs
        await self.make_request(
            session, "GET", f"{self.base_url}:8008/api/v1/workers/jobs",
            "workers", "/api/v1/workers/jobs", headers=headers
        )
        
        # Get templates
        await self.make_request(
            session, "GET", f"{self.base_url}:8008/api/v1/workers/templates",
            "workers", "/api/v1/workers/templates", headers=headers
        )
    
    async def make_request(self, session: aiohttp.ClientSession, method: str, 
                          url: str, service: str, endpoint: str, 
                          headers: Dict = None, data: Dict = None) -> TestResult:
        """Make HTTP request and record test result"""
        start_time = time.time()
        
        try:
            kwargs = {}
            if headers:
                kwargs["headers"] = headers
            if data:
                kwargs["json"] = data
            
            async with session.request(method, url, **kwargs) as response:
                response_time = (time.time() - start_time) * 1000  # ms
                response_data = await response.json() if response.content_type == 'application/json' else await response.text()
                
                success = 200 <= response.status < 300
                
                result = TestResult(
                    service=service,
                    endpoint=endpoint,
                    method=method,
                    status_code=response.status,
                    response_time=response_time,
                    success=success,
                    response_data=response_data if success else None,
                    error_message=str(response_data) if not success else ""
                )
                
                status_icon = "✅" if success else "❌"
                print(f"{status_icon} {service.upper():<12} {method:<6} {endpoint:<30} [{response.status}] {response_time:.0f}ms")
                
                self.test_results.append(result)
                return result
                
        except Exception as e:
            response_time = (time.time() - start_time) * 1000
            result = TestResult(
                service=service,
                endpoint=endpoint,
                method=method,
                status_code=0,
                response_time=response_time,
                success=False,
                error_message=str(e)
            )
            
            print(f"❌ {service.upper():<12} {method:<6} {endpoint:<30} [ERROR] {str(e)}")
            self.test_results.append(result)
            return result
    
    def print_test_summary(self):
        """Print comprehensive test summary"""
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        
        total_tests = len(self.test_results)
        successful_tests = sum(1 for r in self.test_results if r.success)
        failed_tests = total_tests - successful_tests
        
        print(f"Total Tests: {total_tests}")
        print(f"✅ Successful: {successful_tests}")
        print(f"❌ Failed: {failed_tests}")
        print(f"Success Rate: {(successful_tests/total_tests*100):.1f}%")
        
        # Service breakdown
        services = {}
        for result in self.test_results:
            if result.service not in services:
                services[result.service] = {"total": 0, "success": 0}
            services[result.service]["total"] += 1
            if result.success:
                services[result.service]["success"] += 1
        
        print("\n📋 SERVICE BREAKDOWN:")
        for service, stats in services.items():
            rate = (stats["success"] / stats["total"] * 100)
            status_icon = "✅" if rate == 100 else "⚠️" if rate >= 50 else "❌"
            print(f"{status_icon} {service.upper():<15} {stats['success']}/{stats['total']} ({rate:.1f}%)")
        
        # Failed tests detail
        if failed_tests > 0:
            print(f"\n❌ FAILED TESTS:")
            for result in self.test_results:
                if not result.success:
                    print(f"   {result.service} {result.method} {result.endpoint} - {result.error_message}")
        
        print(f"\n✨ Integration Testing Complete - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

async def main():
    """Main test runner"""
    tester = VetrAIAPITester()
    await tester.run_all_tests()

if __name__ == "__main__":
    asyncio.run(main())