#!/usr/bin/env python3
"""
VetrAI Platform Screenshot Capture Script

This script automatically captures screenshots of the VetrAI platform's
frontend and backend interfaces.

Requirements:
    pip install playwright
    playwright install chromium

Usage:
    python scripts/capture_screenshots.py
"""

import os
import sys
import time
import requests
from pathlib import Path

def check_service_health(url, service_name, max_retries=5, delay=2):
    """Check if a service is healthy and responding"""
    print(f"Checking {service_name}...", end=" ")
    for i in range(max_retries):
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                print("✓ Ready")
                return True
        except requests.exceptions.RequestException:
            pass
        
        if i < max_retries - 1:
            time.sleep(delay)
    
    print("✗ Not available")
    return False

def check_playwright():
    """Check if Playwright is installed"""
    try:
        from playwright.sync_api import sync_playwright
        return True
    except ImportError:
        print("❌ Playwright is not installed!")
        print("Install it with:")
        print("  pip install playwright")
        print("  playwright install chromium")
        return False

def capture_screenshots():
    """Capture all screenshots"""
    from playwright.sync_api import sync_playwright
    
    base_dir = Path(__file__).parent.parent
    screenshots_dir = base_dir / "docs" / "screenshots"
    frontend_dir = screenshots_dir / "frontend"
    backend_dir = screenshots_dir / "backend"
    
    # Ensure directories exist
    frontend_dir.mkdir(parents=True, exist_ok=True)
    backend_dir.mkdir(parents=True, exist_ok=True)
    
    print("\n" + "="*60)
    print("🚀 VetrAI Platform Screenshot Capture")
    print("="*60 + "\n")
    
    # Check if services are running
    services_to_check = {
        "Studio Frontend": "http://localhost:3000",
        "Admin Dashboard": "http://localhost:3001",
        "Auth Service": "http://localhost:8001/health",
        "Tenancy Service": "http://localhost:8002/health",
    }
    
    print("Checking service availability...\n")
    all_ready = True
    for name, url in services_to_check.items():
        if not check_service_health(url, name):
            all_ready = False
    
    if not all_ready:
        print("\n⚠️  Some services are not ready!")
        print("Please start the platform with: docker compose up -d")
        print("Wait for all services to be healthy, then run this script again.")
        return False
    
    print("\n✓ All services are ready!\n")
    print("Starting screenshot capture...\n")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            device_scale_factor=1
        )
        page = context.new_page()
        
        # Frontend screenshots
        print("📱 Capturing Frontend Screenshots...")
        
        frontend_pages = [
            ("http://localhost:3000", "studio-dashboard.png", "Studio Dashboard"),
            ("http://localhost:3001", "admin-dashboard.png", "Admin Dashboard"),
        ]
        
        for url, filename, description in frontend_pages:
            try:
                print(f"  • {description}...", end=" ")
                page.goto(url, wait_until="networkidle", timeout=10000)
                time.sleep(2)  # Give time for dynamic content to load
                page.screenshot(path=str(frontend_dir / filename), full_page=False)
                print("✓")
            except Exception as e:
                print(f"✗ Error: {e}")
        
        # Backend API screenshots
        print("\n🔧 Capturing Backend API Screenshots...")
        
        backend_services = [
            (8001, "api-auth.png", "Auth Service"),
            (8002, "api-tenancy.png", "Tenancy Service"),
            (8003, "api-keys.png", "Keys Service"),
            (8004, "api-billing.png", "Billing Service"),
            (8005, "api-support.png", "Support Service"),
            (8006, "api-themes.png", "Themes Service"),
            (8007, "api-notifications.png", "Notifications Service"),
            (8008, "api-workers.png", "Workers Service"),
        ]
        
        for port, filename, description in backend_services:
            try:
                print(f"  • {description}...", end=" ")
                url = f"http://localhost:{port}/docs"
                page.goto(url, wait_until="networkidle", timeout=10000)
                time.sleep(1)
                page.screenshot(path=str(backend_dir / filename), full_page=True)
                print("✓")
            except Exception as e:
                print(f"✗ Error: {e}")
        
        browser.close()
    
    print("\n" + "="*60)
    print("✅ Screenshot capture complete!")
    print("="*60)
    print(f"\nScreenshots saved to:")
    print(f"  Frontend: {frontend_dir}")
    print(f"  Backend: {backend_dir}")
    print("\nNext steps:")
    print("  1. Review the captured screenshots")
    print("  2. Update docs/SCREENSHOTS.md with actual descriptions")
    print("  3. Commit the screenshots to the repository")
    
    return True

def main():
    """Main entry point"""
    # Check if Playwright is installed
    if not check_playwright():
        sys.exit(1)
    
    # Capture screenshots
    success = capture_screenshots()
    
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()
