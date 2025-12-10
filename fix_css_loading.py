#!/usr/bin/env python3
"""
VetrAI Frontend CSS Loading Fix
Addresses common CSS loading issues in Next.js applications
"""

import subprocess
import json
import os
import requests
import time
from pathlib import Path

def print_header(title):
    print(f"\n{'='*50}")
    print(f"🎨 {title}")
    print(f"{'='*50}")

def print_step(step, description):
    print(f"\n{step} {description}")
    print("-" * 40)

def check_frontend_processes():
    """Check if frontend development servers are running"""
    print_step("🔍", "CHECKING FRONTEND PROCESSES")
    
    try:
        # Check for Node.js processes
        result = subprocess.run([
            'powershell', '-Command', 
            'Get-Process | Where-Object {$_.ProcessName -like "*node*"} | Select-Object ProcessName, Id, StartTime'
        ], capture_output=True, text=True)
        
        if result.returncode == 0 and result.stdout.strip():
            print("✅ Node.js processes found:")
            print(result.stdout)
            return True
        else:
            print("❌ No Node.js processes found")
            return False
    except Exception as e:
        print(f"❌ Error checking processes: {e}")
        return False

def check_frontend_ports():
    """Check if frontend ports are responding"""
    print_step("🌐", "TESTING FRONTEND PORTS")
    
    ports = {
        3000: "Studio UI",
        3001: "Admin Dashboard"
    }
    
    working_ports = []
    
    for port, name in ports.items():
        try:
            response = requests.get(f"http://localhost:{port}", timeout=5)
            if response.status_code == 200:
                print(f"✅ {name} (:{port}): OK")
                working_ports.append(port)
            else:
                print(f"⚠️ {name} (:{port}): Status {response.status_code}")
        except requests.ConnectionError:
            print(f"❌ {name} (:{port}): Connection refused")
        except Exception as e:
            print(f"❌ {name} (:{port}): {e}")
    
    return working_ports

def restart_frontend_dev_servers():
    """Restart frontend development servers"""
    print_step("🔄", "RESTARTING FRONTEND SERVERS")
    
    # Kill existing Node.js processes
    try:
        subprocess.run([
            'powershell', '-Command', 
            'Get-Process | Where-Object {$_.ProcessName -like "*node*"} | Stop-Process -Force'
        ], capture_output=True)
        print("✅ Stopped existing Node.js processes")
    except Exception as e:
        print(f"⚠️ Error stopping processes: {e}")
    
    time.sleep(2)
    
    # Start Studio UI
    try:
        studio_path = Path("frontend/studio")
        if studio_path.exists():
            print("🚀 Starting Studio UI...")
            subprocess.Popen([
                'powershell', '-Command', 
                f'cd {studio_path}; npm run dev'
            ], creationflags=subprocess.CREATE_NEW_CONSOLE)
        else:
            print("❌ Studio UI path not found")
    except Exception as e:
        print(f"❌ Failed to start Studio UI: {e}")
    
    # Start Admin Dashboard  
    try:
        admin_path = Path("frontend/admin")
        if admin_path.exists():
            print("🚀 Starting Admin Dashboard...")
            subprocess.Popen([
                'powershell', '-Command', 
                f'cd {admin_path}; npm run dev'
            ], creationflags=subprocess.CREATE_NEW_CONSOLE)
        else:
            print("❌ Admin Dashboard path not found")
    except Exception as e:
        print(f"❌ Failed to start Admin Dashboard: {e}")
    
    print("⏳ Waiting 10 seconds for servers to start...")
    time.sleep(10)

def clear_next_cache():
    """Clear Next.js cache and build artifacts"""
    print_step("🧹", "CLEARING NEXT.JS CACHE")
    
    frontend_dirs = ["frontend/studio", "frontend/admin"]
    
    for frontend_dir in frontend_dirs:
        if Path(frontend_dir).exists():
            print(f"🧹 Clearing cache for {frontend_dir}...")
            
            # Clear .next directory
            next_dir = Path(frontend_dir) / ".next"
            if next_dir.exists():
                try:
                    subprocess.run([
                        'powershell', '-Command', 
                        f'Remove-Item -Recurse -Force "{next_dir}"'
                    ], check=True)
                    print(f"  ✅ Cleared .next cache")
                except Exception as e:
                    print(f"  ⚠️ Error clearing .next: {e}")
            
            # Clear node_modules/.cache
            cache_dir = Path(frontend_dir) / "node_modules" / ".cache"
            if cache_dir.exists():
                try:
                    subprocess.run([
                        'powershell', '-Command', 
                        f'Remove-Item -Recurse -Force "{cache_dir}"'
                    ], check=True)
                    print(f"  ✅ Cleared node_modules cache")
                except Exception as e:
                    print(f"  ⚠️ Error clearing node cache: {e}")

def fix_css_imports():
    """Fix common CSS import issues"""
    print_step("🔧", "FIXING CSS IMPORTS")
    
    frontend_dirs = ["frontend/studio", "frontend/admin"]
    
    for frontend_dir in frontend_dirs:
        app_file = Path(frontend_dir) / "src" / "pages" / "_app.tsx"
        
        if app_file.exists():
            print(f"🔍 Checking {app_file}")
            
            with open(app_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check if globals.css import exists and is correct
            if '@/styles/globals.css' in content:
                print(f"  ✅ CSS import found in {frontend_dir}")
            else:
                print(f"  ⚠️ CSS import might be missing in {frontend_dir}")
                
                # Add CSS import if missing
                if "import '@/styles/globals.css'" not in content:
                    lines = content.split('\n')
                    # Insert CSS import at the beginning
                    lines.insert(0, "import '@/styles/globals.css';")
                    
                    try:
                        with open(app_file, 'w', encoding='utf-8') as f:
                            f.write('\n'.join(lines))
                        print(f"  ✅ Added CSS import to {frontend_dir}")
                    except Exception as e:
                        print(f"  ❌ Failed to fix CSS import: {e}")

def check_tailwind_config():
    """Verify Tailwind CSS configuration"""
    print_step("🎯", "CHECKING TAILWIND CONFIG")
    
    frontend_dirs = ["frontend/studio", "frontend/admin"]
    
    for frontend_dir in frontend_dirs:
        tailwind_config = Path(frontend_dir) / "tailwind.config.js"
        
        if tailwind_config.exists():
            print(f"✅ Tailwind config found: {frontend_dir}")
            
            # Check if content paths are correct
            with open(tailwind_config, 'r', encoding='utf-8') as f:
                config_content = f.read()
            
            if './src/' in config_content:
                print(f"  ✅ Tailwind content paths look correct")
            else:
                print(f"  ⚠️ Tailwind content paths might need fixing")
        else:
            print(f"❌ Tailwind config missing: {frontend_dir}")

def create_quick_fix_commands():
    """Create a quick fix script for common issues"""
    print_step("📝", "CREATING QUICK FIX COMMANDS")
    
    fix_script = """@echo off
echo 🎨 VetrAI CSS Quick Fix
echo ========================

echo 🧹 Clearing Next.js cache...
cd frontend\\studio
if exist .next rmdir /s /q .next
if exist node_modules\\.cache rmdir /s /q node_modules\\.cache

cd ..\\admin
if exist .next rmdir /s /q .next
if exist node_modules\\.cache rmdir /s /q node_modules\\.cache

echo 🔄 Restarting development servers...
cd ..\\..

echo 🚀 Starting Studio UI...
start "Studio UI" cmd /k "cd frontend\\studio && npm run dev"

echo 🚀 Starting Admin Dashboard...  
start "Admin Dashboard" cmd /k "cd frontend\\admin && npm run dev"

echo ✅ Fix complete! Check http://localhost:3000 and http://localhost:3001

pause
"""
    
    with open("fix_css.bat", "w") as f:
        f.write(fix_script)
    
    print("✅ Created fix_css.bat - run this for quick CSS fixes")

def main():
    """Main function"""
    print_header("VETRAI CSS LOADING FIX")
    
    # Check current status
    processes_running = check_frontend_processes()
    working_ports = check_frontend_ports()
    
    if len(working_ports) >= 2:
        print("\n🎉 Both frontends appear to be working!")
        print("💡 If you're still seeing CSS issues, try:")
        print("   1. Clear your browser cache (Ctrl+F5)")
        print("   2. Check browser developer console for errors")
        print("   3. Try incognito/private browsing mode")
    else:
        print("\n🔧 Applying fixes...")
        
        # Apply fixes
        clear_next_cache()
        fix_css_imports()
        check_tailwind_config()
        
        # Restart servers if needed
        if not processes_running or len(working_ports) < 2:
            restart_frontend_dev_servers()
            
            # Check again after restart
            working_ports = check_frontend_ports()
    
    # Always create quick fix commands
    create_quick_fix_commands()
    
    # Final status
    print_header("CSS FIX COMPLETE")
    
    if len(working_ports) >= 2:
        print("🎉 SUCCESS! Both frontends should be working:")
        print("   🔗 Studio UI: http://localhost:3000")
        print("   🔗 Admin Dashboard: http://localhost:3001")
        print("   🧪 CSS Test: Open css_test.html in your browser")
    else:
        print("⚠️ Some issues remain. Try:")
        print("   1. Run: fix_css.bat")
        print("   2. Check: css_test.html")
        print("   3. Manually restart: cd frontend/studio && npm run dev")
    
    print("\n📚 Additional debugging:")
    print("   • Open browser developer tools (F12)")
    print("   • Check Console and Network tabs for errors")
    print("   • Look for failed CSS file requests")

if __name__ == "__main__":
    main()