#!/usr/bin/env python3
"""
VetrAI Platform - End-to-End Testing Suite
Comprehensive E2E testing for the entire VetrAI platform
"""

import asyncio
import aiohttp
import pytest
import json
import time
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class TestResult:
    test_name: str
    status: str
    duration: float
    details: Optional[str] = None
    error: Optional[str] = None

class VetrAIE2ETester:
    """End-to-end testing suite for VetrAI platform"""
    
    def __init__(self):
        self.base_urls = {
            'studio': 'http://localhost:3000',
            'admin': 'http://localhost:3001',
            'auth': 'http://localhost:8001',
            'tenancy': 'http://localhost:8002',
            'workers': 'http://localhost:8003',
            'models': 'http://localhost:8004',
            'agents': 'http://localhost:8005',
            'workflows': 'http://localhost:8006',
            'integrations': 'http://localhost:8007',
            'analytics': 'http://localhost:8008'
        }
        self.test_results: List[TestResult] = []
        self.auth_token: Optional[str] = None
        self.test_user_id: Optional[str] = None
        self.test_tenant_id: Optional[str] = None
    
    async def run_all_tests(self) -> Dict[str, Any]:
        """Run complete end-to-end testing suite"""
        print("🧪 VetrAI Platform - End-to-End Testing Suite")
        print("=" * 60)
        
        start_time = time.time()
        
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=30)) as session:
            # Phase 1: Infrastructure & Service Health
            await self.test_infrastructure_health(session)
            
            # Phase 2: Authentication & User Management
            await self.test_authentication_flow(session)
            
            # Phase 3: Tenant Management
            await self.test_tenant_management(session)
            
            # Phase 4: AI Worker Operations
            await self.test_worker_operations(session)
            
            # Phase 5: Model Management
            await self.test_model_management(session)
            
            # Phase 6: Agent & Workflow Operations
            await self.test_agent_workflows(session)
            
            # Phase 7: Integration Testing
            await self.test_integrations(session)
            
            # Phase 8: Analytics & Reporting
            await self.test_analytics(session)
            
            # Phase 9: Frontend Application Testing
            await self.test_frontend_applications(session)
            
            # Phase 10: Performance & Load Testing
            await self.test_performance(session)
        
        total_duration = time.time() - start_time
        return self.generate_test_report(total_duration)
    
    async def test_infrastructure_health(self, session: aiohttp.ClientSession):
        """Test infrastructure and service health"""
        print("\n🏥 Testing Infrastructure Health...")
        
        # Test all service health endpoints
        for service, base_url in self.base_urls.items():
            start_time = time.time()
            try:
                async with session.get(f"{base_url}/health") as response:
                    duration = time.time() - start_time
                    if response.status == 200:
                        data = await response.json()
                        self.test_results.append(TestResult(
                            f"Health Check - {service.title()}",
                            "PASSED",
                            duration,
                            f"Status: {data.get('status', 'healthy')}"
                        ))
                        print(f"   ✅ {service.title()} Service: Healthy ({duration:.2f}s)")
                    else:
                        self.test_results.append(TestResult(
                            f"Health Check - {service.title()}",
                            "FAILED",
                            duration,
                            error=f"HTTP {response.status}"
                        ))
                        print(f"   ❌ {service.title()} Service: Failed (HTTP {response.status})")
            except Exception as e:
                duration = time.time() - start_time
                self.test_results.append(TestResult(
                    f"Health Check - {service.title()}",
                    "FAILED",
                    duration,
                    error=str(e)
                ))
                print(f"   ❌ {service.title()} Service: Error ({str(e)[:50]}...)")
    
    async def test_authentication_flow(self, session: aiohttp.ClientSession):
        """Test authentication and authorization flow"""
        print("\n🔐 Testing Authentication Flow...")
        
        # Test user registration
        await self.test_user_registration(session)
        
        # Test user login
        await self.test_user_login(session)
        
        # Test token validation
        await self.test_token_validation(session)
        
        # Test logout
        await self.test_user_logout(session)
    
    async def test_user_registration(self, session: aiohttp.ClientSession):
        """Test user registration"""
        start_time = time.time()
        try:
            test_user = {
                "email": "test@vetrai.com",
                "password": "TestPassword123!",
                "name": "Test User",
                "role": "admin"
            }
            
            async with session.post(
                f"{self.base_urls['auth']}/api/v1/register",
                json=test_user
            ) as response:
                duration = time.time() - start_time
                
                if response.status == 201:
                    data = await response.json()
                    self.test_user_id = data.get('user_id')
                    self.test_results.append(TestResult(
                        "User Registration",
                        "PASSED",
                        duration,
                        f"User ID: {self.test_user_id}"
                    ))
                    print(f"   ✅ User Registration: Success ({duration:.2f}s)")
                else:
                    error_data = await response.text()
                    self.test_results.append(TestResult(
                        "User Registration",
                        "FAILED",
                        duration,
                        error=f"HTTP {response.status}: {error_data}"
                    ))
                    print(f"   ❌ User Registration: Failed (HTTP {response.status})")
        
        except Exception as e:
            duration = time.time() - start_time
            self.test_results.append(TestResult(
                "User Registration",
                "FAILED",
                duration,
                error=str(e)
            ))
            print(f"   ❌ User Registration: Error ({str(e)[:50]}...)")
    
    async def test_user_login(self, session: aiohttp.ClientSession):
        """Test user login"""
        start_time = time.time()
        try:
            login_data = {
                "username": "test@vetrai.com",
                "password": "TestPassword123!"
            }
            
            async with session.post(
                f"{self.base_urls['auth']}/api/v1/login",
                data=login_data
            ) as response:
                duration = time.time() - start_time
                
                if response.status == 200:
                    data = await response.json()
                    self.auth_token = data.get('access_token')
                    self.test_results.append(TestResult(
                        "User Login",
                        "PASSED",
                        duration,
                        "Token acquired successfully"
                    ))
                    print(f"   ✅ User Login: Success ({duration:.2f}s)")
                else:
                    error_data = await response.text()
                    self.test_results.append(TestResult(
                        "User Login",
                        "FAILED",
                        duration,
                        error=f"HTTP {response.status}: {error_data}"
                    ))
                    print(f"   ❌ User Login: Failed (HTTP {response.status})")
        
        except Exception as e:
            duration = time.time() - start_time
            self.test_results.append(TestResult(
                "User Login",
                "FAILED",
                duration,
                error=str(e)
            ))
            print(f"   ❌ User Login: Error ({str(e)[:50]}...)")
    
    async def test_token_validation(self, session: aiohttp.ClientSession):
        """Test token validation"""
        if not self.auth_token:
            print("   ⏭️ Token Validation: Skipped (no token available)")
            return
        
        start_time = time.time()
        try:
            headers = {"Authorization": f"Bearer {self.auth_token}"}
            
            async with session.get(
                f"{self.base_urls['auth']}/api/v1/me",
                headers=headers
            ) as response:
                duration = time.time() - start_time
                
                if response.status == 200:
                    data = await response.json()
                    self.test_results.append(TestResult(
                        "Token Validation",
                        "PASSED",
                        duration,
                        f"User: {data.get('email', 'Unknown')}"
                    ))
                    print(f"   ✅ Token Validation: Success ({duration:.2f}s)")
                else:
                    self.test_results.append(TestResult(
                        "Token Validation",
                        "FAILED",
                        duration,
                        error=f"HTTP {response.status}"
                    ))
                    print(f"   ❌ Token Validation: Failed (HTTP {response.status})")
        
        except Exception as e:
            duration = time.time() - start_time
            self.test_results.append(TestResult(
                "Token Validation",
                "FAILED",
                duration,
                error=str(e)
            ))
            print(f"   ❌ Token Validation: Error ({str(e)[:50]}...)")
    
    async def test_user_logout(self, session: aiohttp.ClientSession):
        """Test user logout"""
        if not self.auth_token:
            print("   ⏭️ User Logout: Skipped (no token available)")
            return
        
        start_time = time.time()
        try:
            headers = {"Authorization": f"Bearer {self.auth_token}"}
            
            async with session.post(
                f"{self.base_urls['auth']}/api/v1/logout",
                headers=headers
            ) as response:
                duration = time.time() - start_time
                
                if response.status == 200:
                    self.test_results.append(TestResult(
                        "User Logout",
                        "PASSED",
                        duration,
                        "Token invalidated successfully"
                    ))
                    print(f"   ✅ User Logout: Success ({duration:.2f}s)")
                else:
                    self.test_results.append(TestResult(
                        "User Logout",
                        "FAILED",
                        duration,
                        error=f"HTTP {response.status}"
                    ))
                    print(f"   ❌ User Logout: Failed (HTTP {response.status})")
        
        except Exception as e:
            duration = time.time() - start_time
            self.test_results.append(TestResult(
                "User Logout",
                "FAILED",
                duration,
                error=str(e)
            ))
            print(f"   ❌ User Logout: Error ({str(e)[:50]}...)")
    
    async def test_tenant_management(self, session: aiohttp.ClientSession):
        """Test tenant management operations"""
        print("\n🏢 Testing Tenant Management...")
        
        if not self.auth_token:
            print("   ⏭️ Tenant Management: Skipped (authentication required)")
            return
        
        headers = {"Authorization": f"Bearer {self.auth_token}"}
        
        # Test tenant creation
        start_time = time.time()
        try:
            tenant_data = {
                "name": "Test Tenant",
                "description": "E2E Test Tenant",
                "settings": {"ai_model": "gpt-4"}
            }
            
            async with session.post(
                f"{self.base_urls['tenancy']}/api/v1/tenants",
                json=tenant_data,
                headers=headers
            ) as response:
                duration = time.time() - start_time
                
                if response.status == 201:
                    data = await response.json()
                    self.test_tenant_id = data.get('id')
                    self.test_results.append(TestResult(
                        "Tenant Creation",
                        "PASSED",
                        duration,
                        f"Tenant ID: {self.test_tenant_id}"
                    ))
                    print(f"   ✅ Tenant Creation: Success ({duration:.2f}s)")
                else:
                    self.test_results.append(TestResult(
                        "Tenant Creation",
                        "FAILED",
                        duration,
                        error=f"HTTP {response.status}"
                    ))
                    print(f"   ❌ Tenant Creation: Failed (HTTP {response.status})")
        
        except Exception as e:
            duration = time.time() - start_time
            self.test_results.append(TestResult(
                "Tenant Creation",
                "FAILED",
                duration,
                error=str(e)
            ))
            print(f"   ❌ Tenant Creation: Error ({str(e)[:50]}...)")
    
    async def test_worker_operations(self, session: aiohttp.ClientSession):
        """Test AI worker operations"""
        print("\n🤖 Testing Worker Operations...")
        
        if not self.auth_token:
            print("   ⏭️ Worker Operations: Skipped (authentication required)")
            return
        
        headers = {"Authorization": f"Bearer {self.auth_token}"}
        
        # Test worker listing
        await self.test_worker_listing(session, headers)
        
        # Test worker creation
        await self.test_worker_creation(session, headers)
    
    async def test_worker_listing(self, session: aiohttp.ClientSession, headers: Dict[str, str]):
        """Test worker listing"""
        start_time = time.time()
        try:
            async with session.get(
                f"{self.base_urls['workers']}/api/v1/workers",
                headers=headers
            ) as response:
                duration = time.time() - start_time
                
                if response.status == 200:
                    data = await response.json()
                    worker_count = len(data.get('workers', []))
                    self.test_results.append(TestResult(
                        "Worker Listing",
                        "PASSED",
                        duration,
                        f"Found {worker_count} workers"
                    ))
                    print(f"   ✅ Worker Listing: Success ({worker_count} workers, {duration:.2f}s)")
                else:
                    self.test_results.append(TestResult(
                        "Worker Listing",
                        "FAILED",
                        duration,
                        error=f"HTTP {response.status}"
                    ))
                    print(f"   ❌ Worker Listing: Failed (HTTP {response.status})")
        
        except Exception as e:
            duration = time.time() - start_time
            self.test_results.append(TestResult(
                "Worker Listing",
                "FAILED",
                duration,
                error=str(e)
            ))
            print(f"   ❌ Worker Listing: Error ({str(e)[:50]}...)")
    
    async def test_worker_creation(self, session: aiohttp.ClientSession, headers: Dict[str, str]):
        """Test worker creation"""
        start_time = time.time()
        try:
            worker_data = {
                "name": "Test AI Worker",
                "description": "E2E Test Worker",
                "type": "text_generation",
                "config": {
                    "model": "gpt-4",
                    "temperature": 0.7
                }
            }
            
            async with session.post(
                f"{self.base_urls['workers']}/api/v1/workers",
                json=worker_data,
                headers=headers
            ) as response:
                duration = time.time() - start_time
                
                if response.status == 201:
                    data = await response.json()
                    worker_id = data.get('id')
                    self.test_results.append(TestResult(
                        "Worker Creation",
                        "PASSED",
                        duration,
                        f"Worker ID: {worker_id}"
                    ))
                    print(f"   ✅ Worker Creation: Success ({duration:.2f}s)")
                else:
                    self.test_results.append(TestResult(
                        "Worker Creation",
                        "FAILED",
                        duration,
                        error=f"HTTP {response.status}"
                    ))
                    print(f"   ❌ Worker Creation: Failed (HTTP {response.status})")
        
        except Exception as e:
            duration = time.time() - start_time
            self.test_results.append(TestResult(
                "Worker Creation",
                "FAILED",
                duration,
                error=str(e)
            ))
            print(f"   ❌ Worker Creation: Error ({str(e)[:50]}...)")
    
    async def test_model_management(self, session: aiohttp.ClientSession):
        """Test model management operations"""
        print("\n🧠 Testing Model Management...")
        
        if not self.auth_token:
            print("   ⏭️ Model Management: Skipped (authentication required)")
            return
        
        headers = {"Authorization": f"Bearer {self.auth_token}"}
        
        # Test model listing
        start_time = time.time()
        try:
            async with session.get(
                f"{self.base_urls['models']}/api/v1/models",
                headers=headers
            ) as response:
                duration = time.time() - start_time
                
                if response.status == 200:
                    data = await response.json()
                    model_count = len(data.get('models', []))
                    self.test_results.append(TestResult(
                        "Model Listing",
                        "PASSED",
                        duration,
                        f"Found {model_count} models"
                    ))
                    print(f"   ✅ Model Listing: Success ({model_count} models, {duration:.2f}s)")
                else:
                    self.test_results.append(TestResult(
                        "Model Listing",
                        "FAILED",
                        duration,
                        error=f"HTTP {response.status}"
                    ))
                    print(f"   ❌ Model Listing: Failed (HTTP {response.status})")
        
        except Exception as e:
            duration = time.time() - start_time
            self.test_results.append(TestResult(
                "Model Listing",
                "FAILED",
                duration,
                error=str(e)
            ))
            print(f"   ❌ Model Listing: Error ({str(e)[:50]}...)")
    
    async def test_agent_workflows(self, session: aiohttp.ClientSession):
        """Test agent and workflow operations"""
        print("\n🔄 Testing Agent & Workflow Operations...")
        
        if not self.auth_token:
            print("   ⏭️ Agent & Workflow Operations: Skipped (authentication required)")
            return
        
        headers = {"Authorization": f"Bearer {self.auth_token}"}
        
        # Test agent operations
        await self.test_agents(session, headers)
        
        # Test workflow operations
        await self.test_workflows(session, headers)
    
    async def test_agents(self, session: aiohttp.ClientSession, headers: Dict[str, str]):
        """Test agent operations"""
        start_time = time.time()
        try:
            async with session.get(
                f"{self.base_urls['agents']}/api/v1/agents",
                headers=headers
            ) as response:
                duration = time.time() - start_time
                
                if response.status == 200:
                    data = await response.json()
                    agent_count = len(data.get('agents', []))
                    self.test_results.append(TestResult(
                        "Agent Operations",
                        "PASSED",
                        duration,
                        f"Found {agent_count} agents"
                    ))
                    print(f"   ✅ Agent Operations: Success ({agent_count} agents, {duration:.2f}s)")
                else:
                    self.test_results.append(TestResult(
                        "Agent Operations",
                        "FAILED",
                        duration,
                        error=f"HTTP {response.status}"
                    ))
                    print(f"   ❌ Agent Operations: Failed (HTTP {response.status})")
        
        except Exception as e:
            duration = time.time() - start_time
            self.test_results.append(TestResult(
                "Agent Operations",
                "FAILED",
                duration,
                error=str(e)
            ))
            print(f"   ❌ Agent Operations: Error ({str(e)[:50]}...)")
    
    async def test_workflows(self, session: aiohttp.ClientSession, headers: Dict[str, str]):
        """Test workflow operations"""
        start_time = time.time()
        try:
            async with session.get(
                f"{self.base_urls['workflows']}/api/v1/workflows",
                headers=headers
            ) as response:
                duration = time.time() - start_time
                
                if response.status == 200:
                    data = await response.json()
                    workflow_count = len(data.get('workflows', []))
                    self.test_results.append(TestResult(
                        "Workflow Operations",
                        "PASSED",
                        duration,
                        f"Found {workflow_count} workflows"
                    ))
                    print(f"   ✅ Workflow Operations: Success ({workflow_count} workflows, {duration:.2f}s)")
                else:
                    self.test_results.append(TestResult(
                        "Workflow Operations",
                        "FAILED",
                        duration,
                        error=f"HTTP {response.status}"
                    ))
                    print(f"   ❌ Workflow Operations: Failed (HTTP {response.status})")
        
        except Exception as e:
            duration = time.time() - start_time
            self.test_results.append(TestResult(
                "Workflow Operations",
                "FAILED",
                duration,
                error=str(e)
            ))
            print(f"   ❌ Workflow Operations: Error ({str(e)[:50]}...)")
    
    async def test_integrations(self, session: aiohttp.ClientSession):
        """Test integration operations"""
        print("\n🔗 Testing Integration Operations...")
        
        if not self.auth_token:
            print("   ⏭️ Integration Operations: Skipped (authentication required)")
            return
        
        headers = {"Authorization": f"Bearer {self.auth_token}"}
        
        start_time = time.time()
        try:
            async with session.get(
                f"{self.base_urls['integrations']}/api/v1/integrations",
                headers=headers
            ) as response:
                duration = time.time() - start_time
                
                if response.status == 200:
                    data = await response.json()
                    integration_count = len(data.get('integrations', []))
                    self.test_results.append(TestResult(
                        "Integration Operations",
                        "PASSED",
                        duration,
                        f"Found {integration_count} integrations"
                    ))
                    print(f"   ✅ Integration Operations: Success ({integration_count} integrations, {duration:.2f}s)")
                else:
                    self.test_results.append(TestResult(
                        "Integration Operations",
                        "FAILED",
                        duration,
                        error=f"HTTP {response.status}"
                    ))
                    print(f"   ❌ Integration Operations: Failed (HTTP {response.status})")
        
        except Exception as e:
            duration = time.time() - start_time
            self.test_results.append(TestResult(
                "Integration Operations",
                "FAILED",
                duration,
                error=str(e)
            ))
            print(f"   ❌ Integration Operations: Error ({str(e)[:50]}...)")
    
    async def test_analytics(self, session: aiohttp.ClientSession):
        """Test analytics operations"""
        print("\n📊 Testing Analytics Operations...")
        
        if not self.auth_token:
            print("   ⏭️ Analytics Operations: Skipped (authentication required)")
            return
        
        headers = {"Authorization": f"Bearer {self.auth_token}"}
        
        start_time = time.time()
        try:
            async with session.get(
                f"{self.base_urls['analytics']}/api/v1/metrics",
                headers=headers
            ) as response:
                duration = time.time() - start_time
                
                if response.status == 200:
                    data = await response.json()
                    metrics_count = len(data.get('metrics', []))
                    self.test_results.append(TestResult(
                        "Analytics Operations",
                        "PASSED",
                        duration,
                        f"Found {metrics_count} metrics"
                    ))
                    print(f"   ✅ Analytics Operations: Success ({metrics_count} metrics, {duration:.2f}s)")
                else:
                    self.test_results.append(TestResult(
                        "Analytics Operations",
                        "FAILED",
                        duration,
                        error=f"HTTP {response.status}"
                    ))
                    print(f"   ❌ Analytics Operations: Failed (HTTP {response.status})")
        
        except Exception as e:
            duration = time.time() - start_time
            self.test_results.append(TestResult(
                "Analytics Operations",
                "FAILED",
                duration,
                error=str(e)
            ))
            print(f"   ❌ Analytics Operations: Error ({str(e)[:50]}...)")
    
    async def test_frontend_applications(self, session: aiohttp.ClientSession):
        """Test frontend applications"""
        print("\n🌐 Testing Frontend Applications...")
        
        # Test Studio Frontend
        await self.test_frontend_app(session, "Studio Frontend", self.base_urls['studio'])
        
        # Test Admin Dashboard
        await self.test_frontend_app(session, "Admin Dashboard", self.base_urls['admin'])
    
    async def test_frontend_app(self, session: aiohttp.ClientSession, app_name: str, url: str):
        """Test individual frontend application"""
        start_time = time.time()
        try:
            async with session.get(url) as response:
                duration = time.time() - start_time
                
                if response.status == 200:
                    content = await response.text()
                    # Check if it's a valid HTML response
                    if '<html' in content.lower() and '</html>' in content.lower():
                        self.test_results.append(TestResult(
                            app_name,
                            "PASSED",
                            duration,
                            "Application loaded successfully"
                        ))
                        print(f"   ✅ {app_name}: Success ({duration:.2f}s)")
                    else:
                        self.test_results.append(TestResult(
                            app_name,
                            "FAILED",
                            duration,
                            error="Invalid HTML response"
                        ))
                        print(f"   ❌ {app_name}: Invalid response")
                else:
                    self.test_results.append(TestResult(
                        app_name,
                        "FAILED",
                        duration,
                        error=f"HTTP {response.status}"
                    ))
                    print(f"   ❌ {app_name}: Failed (HTTP {response.status})")
        
        except Exception as e:
            duration = time.time() - start_time
            self.test_results.append(TestResult(
                app_name,
                "FAILED",
                duration,
                error=str(e)
            ))
            print(f"   ❌ {app_name}: Error ({str(e)[:50]}...)")
    
    async def test_performance(self, session: aiohttp.ClientSession):
        """Test performance metrics"""
        print("\n⚡ Testing Performance Metrics...")
        
        # Test concurrent health checks
        start_time = time.time()
        try:
            tasks = []
            for service, base_url in self.base_urls.items():
                if service not in ['studio', 'admin']:  # Skip frontend for concurrency test
                    tasks.append(session.get(f"{base_url}/health"))
            
            responses = await asyncio.gather(*tasks, return_exceptions=True)
            duration = time.time() - start_time
            
            success_count = sum(1 for r in responses if isinstance(r, aiohttp.ClientResponse) and r.status == 200)
            total_count = len(tasks)
            
            self.test_results.append(TestResult(
                "Concurrent Health Checks",
                "PASSED" if success_count == total_count else "PARTIAL",
                duration,
                f"{success_count}/{total_count} services responded successfully"
            ))
            print(f"   ✅ Concurrent Health Checks: {success_count}/{total_count} success ({duration:.2f}s)")
            
            # Close responses
            for response in responses:
                if isinstance(response, aiohttp.ClientResponse):
                    response.close()
        
        except Exception as e:
            duration = time.time() - start_time
            self.test_results.append(TestResult(
                "Concurrent Health Checks",
                "FAILED",
                duration,
                error=str(e)
            ))
            print(f"   ❌ Concurrent Health Checks: Error ({str(e)[:50]}...)")
    
    def generate_test_report(self, total_duration: float) -> Dict[str, Any]:
        """Generate comprehensive test report"""
        print("\n" + "=" * 60)
        print("📋 END-TO-END TESTING REPORT")
        print("=" * 60)
        
        passed_tests = [r for r in self.test_results if r.status == "PASSED"]
        failed_tests = [r for r in self.test_results if r.status == "FAILED"]
        partial_tests = [r for r in self.test_results if r.status == "PARTIAL"]
        
        total_tests = len(self.test_results)
        success_rate = (len(passed_tests) / total_tests * 100) if total_tests > 0 else 0
        
        print(f"Test Summary:")
        print(f"  📊 Total Tests: {total_tests}")
        print(f"  ✅ Passed: {len(passed_tests)}")
        print(f"  ❌ Failed: {len(failed_tests)}")
        print(f"  ⚠️ Partial: {len(partial_tests)}")
        print(f"  📈 Success Rate: {success_rate:.1f}%")
        print(f"  ⏱️ Total Duration: {total_duration:.2f}s")
        
        if failed_tests:
            print(f"\nFailed Tests:")
            for test in failed_tests:
                print(f"  ❌ {test.test_name}: {test.error}")
        
        if partial_tests:
            print(f"\nPartial Tests:")
            for test in partial_tests:
                print(f"  ⚠️ {test.test_name}: {test.details}")
        
        # Performance summary
        avg_duration = sum(r.duration for r in self.test_results) / len(self.test_results)
        print(f"\nPerformance Summary:")
        print(f"  ⚡ Average Response Time: {avg_duration:.3f}s")
        
        fastest_test = min(self.test_results, key=lambda x: x.duration)
        slowest_test = max(self.test_results, key=lambda x: x.duration)
        print(f"  🚀 Fastest Test: {fastest_test.test_name} ({fastest_test.duration:.3f}s)")
        print(f"  🐌 Slowest Test: {slowest_test.test_name} ({slowest_test.duration:.3f}s)")
        
        print(f"\n🎉 VetrAI Platform E2E Testing Complete!")
        print(f"   Platform Status: {'✅ READY' if success_rate >= 80 else '⚠️ NEEDS ATTENTION'}")
        
        return {
            'total_tests': total_tests,
            'passed': len(passed_tests),
            'failed': len(failed_tests),
            'partial': len(partial_tests),
            'success_rate': success_rate,
            'total_duration': total_duration,
            'average_duration': avg_duration,
            'fastest_test': {
                'name': fastest_test.test_name,
                'duration': fastest_test.duration
            },
            'slowest_test': {
                'name': slowest_test.test_name,
                'duration': slowest_test.duration
            },
            'failed_tests': [{'name': t.test_name, 'error': t.error} for t in failed_tests],
            'status': 'READY' if success_rate >= 80 else 'NEEDS_ATTENTION'
        }

async def main():
    """Main E2E testing runner"""
    tester = VetrAIE2ETester()
    report = await tester.run_all_tests()
    
    # Save report to file
    with open('e2e_test_report.json', 'w') as f:
        json.dump(report, f, indent=2)
    
    return 0 if report['success_rate'] >= 80 else 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())