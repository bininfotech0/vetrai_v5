#!/usr/bin/env python3
"""
VetrAI Codebase Analysis Tool

This script performs comprehensive analysis of the VetrAI codebase including:
- Code metrics and statistics
- Service architecture analysis
- Dependency analysis
- Code quality checks
- Security considerations
- Documentation coverage
"""

import os
import sys
import json
import re
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Tuple, Any
import subprocess


class CodeAnalyzer:
    """Main class for analyzing the VetrAI codebase"""
    
    def __init__(self, repo_path: str = "."):
        self.repo_path = Path(repo_path).resolve()
        self.results = {
            "summary": {},
            "code_metrics": {},
            "services": {},
            "dependencies": {},
            "security": {},
            "documentation": {},
            "quality": {}
        }
    
    def analyze(self) -> Dict[str, Any]:
        """Run all analysis tasks"""
        print("🔍 Starting VetrAI Codebase Analysis...")
        print(f"📁 Repository Path: {self.repo_path}\n")
        
        self.analyze_code_metrics()
        self.analyze_services()
        self.analyze_dependencies()
        self.analyze_documentation()
        self.analyze_security()
        self.analyze_code_quality()
        self.generate_summary()
        
        return self.results
    
    def analyze_code_metrics(self):
        """Analyze code metrics including LOC, file counts, etc."""
        print("📊 Analyzing Code Metrics...")
        
        metrics = {
            "total_files": 0,
            "python_files": 0,
            "javascript_files": 0,
            "markdown_files": 0,
            "yaml_files": 0,
            "dockerfile_count": 0,
            "total_lines": 0,
            "python_lines": 0,
            "blank_lines": 0,
            "comment_lines": 0,
            "directories": set()
        }
        
        for root, dirs, files in os.walk(self.repo_path):
            # Skip common exclusions
            dirs[:] = [d for d in dirs if d not in ['.git', '__pycache__', 'node_modules', 
                                                     'venv', '.venv', 'dist', 'build', '.github']]
            
            for file in files:
                file_path = Path(root) / file
                metrics["total_files"] += 1
                
                if file.endswith('.py'):
                    metrics["python_files"] += 1
                    try:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            lines = f.readlines()
                            metrics["python_lines"] += len(lines)
                            for line in lines:
                                stripped = line.strip()
                                if not stripped:
                                    metrics["blank_lines"] += 1
                                elif stripped.startswith('#'):
                                    metrics["comment_lines"] += 1
                    except Exception as e:
                        print(f"  ⚠️  Error reading {file_path}: {e}")
                
                elif file.endswith(('.js', '.jsx', '.ts', '.tsx')):
                    metrics["javascript_files"] += 1
                elif file.endswith('.md'):
                    metrics["markdown_files"] += 1
                elif file.endswith(('.yml', '.yaml')):
                    metrics["yaml_files"] += 1
                elif file.lower() in ['dockerfile', 'dockerfile.dev', 'dockerfile.prod']:
                    metrics["dockerfile_count"] += 1
                
                metrics["directories"].add(Path(root).relative_to(self.repo_path))
        
        metrics["directories"] = len(metrics["directories"])
        metrics["code_lines"] = metrics["python_lines"] - metrics["blank_lines"] - metrics["comment_lines"]
        
        self.results["code_metrics"] = metrics
        print(f"  ✓ Total Files: {metrics['total_files']}")
        print(f"  ✓ Python Files: {metrics['python_files']}")
        print(f"  ✓ Lines of Python Code: {metrics['code_lines']:,}\n")
    
    def analyze_services(self):
        """Analyze microservices architecture"""
        print("🏗️  Analyzing Service Architecture...")
        
        services_path = self.repo_path / "services"
        if not services_path.exists():
            print("  ⚠️  Services directory not found\n")
            return
        
        services = {}
        
        for service_dir in services_path.iterdir():
            if service_dir.is_dir() and service_dir.name != 'shared':
                service_name = service_dir.name
                service_info = {
                    "path": str(service_dir.relative_to(self.repo_path)),
                    "files": [],
                    "endpoints": [],
                    "models": [],
                    "has_dockerfile": False,
                    "has_requirements": False,
                    "has_tests": False,
                    "port": None
                }
                
                # Check for key files
                app_dir = service_dir / "app"
                if app_dir.exists():
                    for file in app_dir.iterdir():
                        if file.is_file() and file.suffix == '.py':
                            service_info["files"].append(file.name)
                            
                            # Analyze routes
                            if file.name == 'routes.py':
                                service_info["endpoints"] = self._extract_endpoints(file)
                            
                            # Analyze models
                            if file.name == 'models.py':
                                service_info["models"] = self._extract_models(file)
                            
                            # Check for port in main.py
                            if file.name == 'main.py':
                                service_info["port"] = self._extract_port(file)
                
                # Check for Dockerfile
                if (service_dir / "Dockerfile").exists():
                    service_info["has_dockerfile"] = True
                
                # Check for requirements
                if (service_dir / "requirements.txt").exists():
                    service_info["has_requirements"] = True
                
                # Check for tests
                tests_dir = service_dir / "tests"
                if tests_dir.exists() and any(tests_dir.iterdir()):
                    service_info["has_tests"] = True
                
                services[service_name] = service_info
        
        self.results["services"] = services
        print(f"  ✓ Found {len(services)} microservices")
        for name, info in services.items():
            status = "✓" if info["has_dockerfile"] and info["has_requirements"] else "⚠"
            print(f"    {status} {name:15} | Port: {info.get('port', 'N/A'):5} | "
                  f"Endpoints: {len(info['endpoints']):2} | Models: {len(info['models']):2}")
        print()
    
    def _extract_endpoints(self, file_path: Path) -> List[str]:
        """Extract API endpoints from routes file"""
        endpoints = []
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                # Look for FastAPI route decorators
                patterns = [
                    r'@router\.(get|post|put|delete|patch)\(["\']([^"\']+)["\']',
                    r'@app\.(get|post|put|delete|patch)\(["\']([^"\']+)["\']'
                ]
                for pattern in patterns:
                    matches = re.findall(pattern, content)
                    for method, path in matches:
                        endpoints.append(f"{method.upper()} {path}")
        except Exception as e:
            pass
        return endpoints
    
    def _extract_models(self, file_path: Path) -> List[str]:
        """Extract SQLAlchemy models from models file"""
        models = []
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                # Look for class definitions that inherit from Base
                pattern = r'class\s+(\w+)\s*\([^)]*Base[^)]*\):'
                matches = re.findall(pattern, content)
                models = matches
        except Exception as e:
            pass
        return models
    
    def _extract_port(self, file_path: Path) -> str:
        """Extract port number from main.py"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                # Look for port in uvicorn.run or similar
                pattern = r'port["\s]*[=:]["\s]*(\d+)'
                match = re.search(pattern, content)
                if match:
                    return match.group(1)
        except Exception as e:
            pass
        return None
    
    def analyze_dependencies(self):
        """Analyze project dependencies"""
        print("📦 Analyzing Dependencies...")
        
        dependencies = {
            "services": {},
            "common_packages": defaultdict(int),
            "version_conflicts": []
        }
        
        services_path = self.repo_path / "services"
        if services_path.exists():
            for service_dir in services_path.iterdir():
                if service_dir.is_dir():
                    req_file = service_dir / "requirements.txt"
                    if req_file.exists():
                        deps = self._parse_requirements(req_file)
                        dependencies["services"][service_dir.name] = deps
                        for pkg, version in deps.items():
                            dependencies["common_packages"][pkg] += 1
        
        # Sort common packages by usage count
        top_packages = sorted(dependencies["common_packages"].items(), 
                            key=lambda x: x[1], reverse=True)[:10]
        
        self.results["dependencies"] = dependencies
        print(f"  ✓ Analyzed {len(dependencies['services'])} service dependencies")
        print(f"  ✓ Top common packages:")
        for pkg, count in top_packages:
            print(f"    - {pkg:20} (used in {count} services)")
        print()
    
    def _parse_requirements(self, file_path: Path) -> Dict[str, str]:
        """Parse requirements.txt file"""
        requirements = {}
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        # Parse package==version or package>=version
                        match = re.match(r'([a-zA-Z0-9\-_]+)\s*([=><!]+)\s*([0-9.]+)', line)
                        if match:
                            pkg, op, version = match.groups()
                            requirements[pkg] = f"{op}{version}"
                        elif '==' not in line and '>=' not in line:
                            requirements[line] = "any"
        except Exception as e:
            pass
        return requirements
    
    def analyze_documentation(self):
        """Analyze documentation coverage"""
        print("📚 Analyzing Documentation...")
        
        docs = {
            "markdown_files": [],
            "readme_found": False,
            "contributing_found": False,
            "api_docs": False,
            "architecture_docs": False,
            "deployment_docs": False,
            "total_doc_lines": 0
        }
        
        # Find all markdown files
        for root, dirs, files in os.walk(self.repo_path):
            dirs[:] = [d for d in dirs if d not in ['.git', 'node_modules', 'venv', '.venv']]
            for file in files:
                if file.endswith('.md'):
                    file_path = Path(root) / file
                    rel_path = file_path.relative_to(self.repo_path)
                    docs["markdown_files"].append(str(rel_path))
                    
                    # Count lines
                    try:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            docs["total_doc_lines"] += len(f.readlines())
                    except:
                        pass
                    
                    # Check for key documentation files
                    if file.upper() == 'README.MD':
                        docs["readme_found"] = True
                    elif file.upper() == 'CONTRIBUTING.MD':
                        docs["contributing_found"] = True
        
        # Check for specific documentation directories
        docs_path = self.repo_path / "docs"
        if docs_path.exists():
            if (docs_path / "api").exists():
                docs["api_docs"] = True
            if (docs_path / "architecture").exists():
                docs["architecture_docs"] = True
            if (docs_path / "deployment").exists():
                docs["deployment_docs"] = True
        
        self.results["documentation"] = docs
        print(f"  ✓ Markdown files: {len(docs['markdown_files'])}")
        print(f"  ✓ Total documentation lines: {docs['total_doc_lines']:,}")
        print(f"  {'✓' if docs['readme_found'] else '✗'} README.md")
        print(f"  {'✓' if docs['contributing_found'] else '✗'} CONTRIBUTING.md")
        print(f"  {'✓' if docs['api_docs'] else '✗'} API Documentation")
        print(f"  {'✓' if docs['architecture_docs'] else '✗'} Architecture Documentation")
        print(f"  {'✓' if docs['deployment_docs'] else '✗'} Deployment Documentation\n")
    
    def analyze_security(self):
        """Analyze security aspects"""
        print("🔒 Analyzing Security...")
        
        security = {
            "env_example_found": False,
            "gitignore_found": False,
            "security_md_found": False,
            "dockerignore_found": False,
            "secrets_in_code": [],
            "hardcoded_urls": [],
            "security_patterns": {
                "jwt_usage": False,
                "password_hashing": False,
                "sql_parameterization": False
            }
        }
        
        # Check for security-related files
        security["env_example_found"] = (self.repo_path / ".env.example").exists()
        security["gitignore_found"] = (self.repo_path / ".gitignore").exists()
        security["security_md_found"] = (self.repo_path / "SECURITY.md").exists()
        security["dockerignore_found"] = (self.repo_path / ".dockerignore").exists()
        
        # Scan Python files for security patterns
        for root, dirs, files in os.walk(self.repo_path / "services"):
            dirs[:] = [d for d in dirs if d not in ['__pycache__', 'venv', '.venv']]
            for file in files:
                if file.endswith('.py'):
                    file_path = Path(root) / file
                    try:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()
                            
                            # Check for JWT usage
                            if 'jwt' in content.lower() or 'jose' in content.lower():
                                security["security_patterns"]["jwt_usage"] = True
                            
                            # Check for password hashing
                            if 'bcrypt' in content.lower() or 'hash_password' in content:
                                security["security_patterns"]["password_hashing"] = True
                            
                            # Check for SQL parameterization (good practice)
                            if 'execute(' in content and '?' in content:
                                security["security_patterns"]["sql_parameterization"] = True
                            
                            # Look for potential hardcoded credentials (basic check)
                            patterns = [
                                r'password\s*=\s*["\'][^"\']+["\']',
                                r'api[_-]?key\s*=\s*["\'][^"\']+["\']',
                                r'secret\s*=\s*["\'][^"\']+["\']'
                            ]
                            for pattern in patterns:
                                matches = re.findall(pattern, content, re.IGNORECASE)
                                if matches:
                                    rel_path = file_path.relative_to(self.repo_path)
                                    # Filter out obvious false positives
                                    if 'example' not in str(rel_path).lower():
                                        security["secrets_in_code"].append(str(rel_path))
                                        break
                    except Exception as e:
                        pass
        
        self.results["security"] = security
        print(f"  {'✓' if security['env_example_found'] else '✗'} .env.example file")
        print(f"  {'✓' if security['gitignore_found'] else '✗'} .gitignore file")
        print(f"  {'✓' if security['security_md_found'] else '✗'} SECURITY.md file")
        print(f"  {'✓' if security['security_patterns']['jwt_usage'] else '✗'} JWT authentication detected")
        print(f"  {'✓' if security['security_patterns']['password_hashing'] else '✗'} Password hashing detected")
        
        if security["secrets_in_code"]:
            print(f"  ⚠️  Potential secrets found in {len(security['secrets_in_code'])} files")
        else:
            print(f"  ✓ No obvious hardcoded secrets detected")
        print()
    
    def analyze_code_quality(self):
        """Analyze code quality aspects"""
        print("✨ Analyzing Code Quality...")
        
        quality = {
            "python_files_with_docstrings": 0,
            "python_files_without_docstrings": 0,
            "files_with_type_hints": 0,
            "test_files": 0,
            "avg_function_length": 0,
            "long_files": []
        }
        
        total_functions = 0
        total_function_lines = 0
        
        for root, dirs, files in os.walk(self.repo_path):
            dirs[:] = [d for d in dirs if d not in ['.git', '__pycache__', 'node_modules', 'venv', '.venv']]
            for file in files:
                if file.endswith('.py'):
                    file_path = Path(root) / file
                    
                    # Count test files
                    if 'test' in file.lower() or file_path.parent.name == 'tests':
                        quality["test_files"] += 1
                    
                    try:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()
                            lines = content.split('\n')
                            
                            # Check for module docstring
                            if content.strip().startswith('"""') or content.strip().startswith("'''"):
                                quality["python_files_with_docstrings"] += 1
                            else:
                                quality["python_files_without_docstrings"] += 1
                            
                            # Check for type hints
                            if '->' in content or ': ' in content:
                                quality["files_with_type_hints"] += 1
                            
                            # Check file length
                            if len(lines) > 500:
                                rel_path = file_path.relative_to(self.repo_path)
                                quality["long_files"].append((str(rel_path), len(lines)))
                            
                            # Count functions and their lengths (basic)
                            func_count = len(re.findall(r'\n\s*def\s+\w+', content))
                            if func_count > 0:
                                total_functions += func_count
                                # Rough estimate
                                total_function_lines += len(lines) / func_count
                    except Exception as e:
                        pass
        
        if total_functions > 0:
            quality["avg_function_length"] = int(total_function_lines / total_functions)
        
        # Sort long files by length
        quality["long_files"] = sorted(quality["long_files"], key=lambda x: x[1], reverse=True)[:10]
        
        self.results["quality"] = quality
        
        total_py_files = quality["python_files_with_docstrings"] + quality["python_files_without_docstrings"]
        if total_py_files > 0:
            docstring_pct = (quality["python_files_with_docstrings"] / total_py_files) * 100
            print(f"  ✓ Module docstrings: {quality['python_files_with_docstrings']}/{total_py_files} ({docstring_pct:.1f}%)")
        
        print(f"  ✓ Files with type hints: {quality['files_with_type_hints']}")
        print(f"  ✓ Test files: {quality['test_files']}")
        print(f"  ✓ Avg function length: ~{quality['avg_function_length']} lines")
        
        if quality["long_files"]:
            print(f"  ⚠️  Long files (>500 lines): {len(quality['long_files'])}")
        print()
    
    def generate_summary(self):
        """Generate overall summary"""
        print("📋 Generating Summary...\n")
        
        summary = {
            "repository": "VetrAI Platform",
            "analysis_date": subprocess.check_output(['date', '+%Y-%m-%d']).decode().strip(),
            "total_services": len(self.results.get("services", {})),
            "total_python_files": self.results["code_metrics"].get("python_files", 0),
            "total_code_lines": self.results["code_metrics"].get("code_lines", 0),
            "documentation_files": len(self.results["documentation"].get("markdown_files", [])),
            "health_score": self._calculate_health_score()
        }
        
        self.results["summary"] = summary
    
    def _calculate_health_score(self) -> int:
        """Calculate overall repository health score (0-100)"""
        score = 0
        
        # Documentation (25 points)
        docs = self.results.get("documentation", {})
        if docs.get("readme_found"):
            score += 5
        if docs.get("contributing_found"):
            score += 5
        if docs.get("api_docs"):
            score += 5
        if docs.get("architecture_docs"):
            score += 5
        if docs.get("deployment_docs"):
            score += 5
        
        # Security (25 points)
        sec = self.results.get("security", {})
        if sec.get("env_example_found"):
            score += 5
        if sec.get("gitignore_found"):
            score += 5
        if sec.get("security_md_found"):
            score += 5
        if sec.get("security_patterns", {}).get("jwt_usage"):
            score += 5
        if sec.get("security_patterns", {}).get("password_hashing"):
            score += 5
        
        # Services (25 points)
        services = self.results.get("services", {})
        if services:
            services_with_docker = sum(1 for s in services.values() if s.get("has_dockerfile"))
            services_with_reqs = sum(1 for s in services.values() if s.get("has_requirements"))
            score += int((services_with_docker / len(services)) * 12.5)
            score += int((services_with_reqs / len(services)) * 12.5)
        
        # Code Quality (25 points)
        quality = self.results.get("quality", {})
        total_py = quality.get("python_files_with_docstrings", 0) + quality.get("python_files_without_docstrings", 0)
        if total_py > 0:
            docstring_score = (quality.get("python_files_with_docstrings", 0) / total_py) * 10
            score += docstring_score
        
        if quality.get("test_files", 0) > 0:
            score += 10
        
        if quality.get("files_with_type_hints", 0) > 0:
            score += 5
        
        return min(int(score), 100)
    
    def generate_report(self, output_file: str = "CODEBASE_ANALYSIS.md"):
        """Generate a markdown report"""
        print(f"📄 Generating Report: {output_file}")
        
        report = []
        report.append("# VetrAI Codebase Analysis Report\n")
        report.append(f"**Generated:** {self.results['summary'].get('analysis_date', 'N/A')}\n")
        report.append(f"**Health Score:** {self.results['summary'].get('health_score', 0)}/100\n")
        report.append("---\n\n")
        
        # Summary
        report.append("## 📊 Summary\n")
        summary = self.results.get("summary", {})
        report.append(f"- **Total Services:** {summary.get('total_services', 0)}\n")
        report.append(f"- **Python Files:** {summary.get('total_python_files', 0)}\n")
        report.append(f"- **Lines of Code:** {summary.get('total_code_lines', 0):,}\n")
        report.append(f"- **Documentation Files:** {summary.get('documentation_files', 0)}\n\n")
        
        # Code Metrics
        report.append("## 📈 Code Metrics\n")
        metrics = self.results.get("code_metrics", {})
        report.append(f"- Total Files: {metrics.get('total_files', 0)}\n")
        report.append(f"- Python Files: {metrics.get('python_files', 0)}\n")
        report.append(f"- JavaScript/TypeScript Files: {metrics.get('javascript_files', 0)}\n")
        report.append(f"- Markdown Files: {metrics.get('markdown_files', 0)}\n")
        report.append(f"- YAML Files: {metrics.get('yaml_files', 0)}\n")
        report.append(f"- Dockerfiles: {metrics.get('dockerfile_count', 0)}\n")
        report.append(f"- Python Code Lines: {metrics.get('code_lines', 0):,}\n")
        report.append(f"- Comment Lines: {metrics.get('comment_lines', 0):,}\n")
        report.append(f"- Blank Lines: {metrics.get('blank_lines', 0):,}\n\n")
        
        # Services
        report.append("## 🏗️ Service Architecture\n")
        services = self.results.get("services", {})
        if services:
            report.append(f"Found **{len(services)}** microservices:\n\n")
            report.append("| Service | Port | Endpoints | Models | Docker | Requirements | Tests |\n")
            report.append("|---------|------|-----------|--------|--------|--------------|-------|\n")
            for name, info in services.items():
                docker = "✓" if info.get("has_dockerfile") else "✗"
                reqs = "✓" if info.get("has_requirements") else "✗"
                tests = "✓" if info.get("has_tests") else "✗"
                port = info.get("port", "N/A")
                endpoints = len(info.get("endpoints", []))
                models = len(info.get("models", []))
                report.append(f"| {name} | {port} | {endpoints} | {models} | {docker} | {reqs} | {tests} |\n")
            report.append("\n")
            
            # Detailed endpoints for each service
            report.append("### Service Endpoints\n")
            for name, info in services.items():
                if info.get("endpoints"):
                    report.append(f"\n**{name.capitalize()} Service**\n")
                    for endpoint in info["endpoints"]:
                        report.append(f"- `{endpoint}`\n")
            report.append("\n")
        
        # Dependencies
        report.append("## 📦 Dependencies\n")
        deps = self.results.get("dependencies", {})
        common = deps.get("common_packages", {})
        if common:
            top = sorted(common.items(), key=lambda x: x[1], reverse=True)[:15]
            report.append("**Most Common Packages:**\n\n")
            for pkg, count in top:
                report.append(f"- `{pkg}` (used in {count} services)\n")
            report.append("\n")
        
        # Documentation
        report.append("## 📚 Documentation\n")
        docs = self.results.get("documentation", {})
        report.append(f"- Total Markdown Files: {len(docs.get('markdown_files', []))}\n")
        report.append(f"- Total Documentation Lines: {docs.get('total_doc_lines', 0):,}\n")
        report.append(f"- README.md: {'✓ Found' if docs.get('readme_found') else '✗ Missing'}\n")
        report.append(f"- CONTRIBUTING.md: {'✓ Found' if docs.get('contributing_found') else '✗ Missing'}\n")
        report.append(f"- API Documentation: {'✓ Found' if docs.get('api_docs') else '✗ Missing'}\n")
        report.append(f"- Architecture Docs: {'✓ Found' if docs.get('architecture_docs') else '✗ Missing'}\n")
        report.append(f"- Deployment Docs: {'✓ Found' if docs.get('deployment_docs') else '✗ Missing'}\n\n")
        
        # Security
        report.append("## 🔒 Security Analysis\n")
        sec = self.results.get("security", {})
        report.append("**Security Files:**\n")
        report.append(f"- .env.example: {'✓' if sec.get('env_example_found') else '✗'}\n")
        report.append(f"- .gitignore: {'✓' if sec.get('gitignore_found') else '✗'}\n")
        report.append(f"- SECURITY.md: {'✓' if sec.get('security_md_found') else '✗'}\n")
        report.append(f"- .dockerignore: {'✓' if sec.get('dockerignore_found') else '✗'}\n\n")
        
        patterns = sec.get("security_patterns", {})
        report.append("**Security Patterns:**\n")
        report.append(f"- JWT Authentication: {'✓ Detected' if patterns.get('jwt_usage') else '✗ Not detected'}\n")
        report.append(f"- Password Hashing: {'✓ Detected' if patterns.get('password_hashing') else '✗ Not detected'}\n\n")
        
        if sec.get("secrets_in_code"):
            report.append(f"⚠️ **Warning:** Potential hardcoded secrets found in {len(sec['secrets_in_code'])} files\n\n")
        
        # Code Quality
        report.append("## ✨ Code Quality\n")
        quality = self.results.get("quality", {})
        total_py = quality.get("python_files_with_docstrings", 0) + quality.get("python_files_without_docstrings", 0)
        if total_py > 0:
            pct = (quality.get("python_files_with_docstrings", 0) / total_py) * 100
            report.append(f"- Files with Docstrings: {quality.get('python_files_with_docstrings', 0)}/{total_py} ({pct:.1f}%)\n")
        report.append(f"- Files with Type Hints: {quality.get('files_with_type_hints', 0)}\n")
        report.append(f"- Test Files: {quality.get('test_files', 0)}\n")
        report.append(f"- Average Function Length: ~{quality.get('avg_function_length', 0)} lines\n\n")
        
        if quality.get("long_files"):
            report.append("**Long Files (>500 lines):**\n")
            for file_path, lines in quality["long_files"][:5]:
                report.append(f"- `{file_path}` ({lines} lines)\n")
            report.append("\n")
        
        # Recommendations
        report.append("## 💡 Recommendations\n")
        recommendations = self._generate_recommendations()
        for rec in recommendations:
            report.append(f"- {rec}\n")
        report.append("\n")
        
        # Save report
        output_path = self.repo_path / output_file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(''.join(report))
        
        print(f"  ✓ Report saved to: {output_path}\n")
    
    def _generate_recommendations(self) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []
        
        # Documentation recommendations
        docs = self.results.get("documentation", {})
        if not docs.get("readme_found"):
            recommendations.append("Add a comprehensive README.md file")
        if not docs.get("api_docs"):
            recommendations.append("Create API documentation in docs/api/")
        if not docs.get("architecture_docs"):
            recommendations.append("Document system architecture in docs/architecture/")
        
        # Security recommendations
        sec = self.results.get("security", {})
        if not sec.get("env_example_found"):
            recommendations.append("Create .env.example file with configuration templates")
        if not sec.get("security_md_found"):
            recommendations.append("Add SECURITY.md file with vulnerability reporting process")
        if sec.get("secrets_in_code"):
            recommendations.append("⚠️ Review and remove hardcoded secrets from source code")
        
        # Service recommendations
        services = self.results.get("services", {})
        services_without_docker = [name for name, info in services.items() 
                                  if not info.get("has_dockerfile")]
        if services_without_docker:
            recommendations.append(f"Add Dockerfiles to services: {', '.join(services_without_docker)}")
        
        services_without_tests = [name for name, info in services.items() 
                                 if not info.get("has_tests")]
        if services_without_tests:
            recommendations.append(f"Add tests to services: {', '.join(services_without_tests)}")
        
        # Code quality recommendations
        quality = self.results.get("quality", {})
        if quality.get("test_files", 0) < 5:
            recommendations.append("Increase test coverage - add more unit and integration tests")
        
        total_py = quality.get("python_files_with_docstrings", 0) + quality.get("python_files_without_docstrings", 0)
        if total_py > 0:
            pct = (quality.get("python_files_with_docstrings", 0) / total_py) * 100
            if pct < 50:
                recommendations.append("Improve documentation - add docstrings to Python modules")
        
        if not recommendations:
            recommendations.append("✓ Codebase is well-maintained! Keep up the good work.")
        
        return recommendations
    
    def save_json(self, output_file: str = "codebase_analysis.json"):
        """Save analysis results as JSON"""
        output_path = self.repo_path / output_file
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, default=str)
        print(f"  ✓ JSON data saved to: {output_path}\n")


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Analyze VetrAI codebase')
    parser.add_argument('--path', default='.', help='Repository path (default: current directory)')
    parser.add_argument('--output', default='CODEBASE_ANALYSIS.md', help='Output report filename')
    parser.add_argument('--json', action='store_true', help='Also save results as JSON')
    parser.add_argument('--verbose', action='store_true', help='Verbose output')
    
    args = parser.parse_args()
    
    # Run analysis
    analyzer = CodeAnalyzer(args.path)
    results = analyzer.analyze()
    
    # Generate reports
    analyzer.generate_report(args.output)
    
    if args.json:
        analyzer.save_json()
    
    # Print final summary
    print("=" * 60)
    print("🎉 Analysis Complete!")
    print("=" * 60)
    summary = results.get("summary", {})
    print(f"Repository Health Score: {summary.get('health_score', 0)}/100")
    print(f"Total Services: {summary.get('total_services', 0)}")
    print(f"Lines of Code: {summary.get('total_code_lines', 0):,}")
    print(f"Documentation Files: {summary.get('documentation_files', 0)}")
    print("=" * 60)


if __name__ == "__main__":
    main()
