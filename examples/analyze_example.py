#!/usr/bin/env python3
"""
Example script demonstrating how to use the VetrAI code analysis tool programmatically.

This shows how to:
1. Import and use the CodeAnalyzer class
2. Access analysis results
3. Generate custom reports
4. Extract specific metrics
"""

import sys
from pathlib import Path

# Add parent directory to path to import the analyzer
sys.path.insert(0, str(Path(__file__).parent.parent))

from analyze_codebase import CodeAnalyzer


def main():
    """Run analysis and demonstrate usage"""
    
    # Initialize analyzer
    repo_path = Path(__file__).parent.parent
    analyzer = CodeAnalyzer(repo_path)
    
    print("=" * 70)
    print("VetrAI Code Analysis - Programmatic Usage Example")
    print("=" * 70)
    print()
    
    # Run analysis
    results = analyzer.analyze()
    
    print("\n" + "=" * 70)
    print("CUSTOM ANALYSIS EXAMPLES")
    print("=" * 70)
    
    # Example 1: Get service information
    print("\n1️⃣  Service Summary:")
    services = results.get("services", {})
    for name, info in services.items():
        print(f"   • {name:15} - {len(info.get('endpoints', []))} endpoints, "
              f"{len(info.get('models', []))} models")
    
    # Example 2: Check documentation coverage
    print("\n2️⃣  Documentation Status:")
    docs = results.get("documentation", {})
    doc_checks = [
        ("README", docs.get("readme_found", False)),
        ("CONTRIBUTING", docs.get("contributing_found", False)),
        ("API Docs", docs.get("api_docs", False)),
        ("Architecture Docs", docs.get("architecture_docs", False)),
        ("Deployment Docs", docs.get("deployment_docs", False))
    ]
    for name, status in doc_checks:
        symbol = "✓" if status else "✗"
        print(f"   {symbol} {name}")
    
    # Example 3: Security overview
    print("\n3️⃣  Security Checklist:")
    security = results.get("security", {})
    sec_patterns = security.get("security_patterns", {})
    security_checks = [
        ("JWT Authentication", sec_patterns.get("jwt_usage", False)),
        ("Password Hashing", sec_patterns.get("password_hashing", False)),
        ("SQL Parameterization", sec_patterns.get("sql_parameterization", False)),
        (".env.example present", security.get("env_example_found", False)),
        (".gitignore present", security.get("gitignore_found", False))
    ]
    for name, status in security_checks:
        symbol = "✓" if status else "✗"
        print(f"   {symbol} {name}")
    
    # Example 4: Code quality metrics
    print("\n4️⃣  Code Quality Metrics:")
    quality = results.get("quality", {})
    metrics = results.get("code_metrics", {})
    
    total_py = quality.get("python_files_with_docstrings", 0) + \
               quality.get("python_files_without_docstrings", 0)
    docstring_pct = (quality.get("python_files_with_docstrings", 0) / total_py * 100) if total_py > 0 else 0
    
    print(f"   • Lines of Code: {metrics.get('code_lines', 0):,}")
    print(f"   • Python Files: {metrics.get('python_files', 0)}")
    print(f"   • Docstring Coverage: {docstring_pct:.1f}%")
    print(f"   • Type Hints: {quality.get('files_with_type_hints', 0)} files")
    print(f"   • Test Files: {quality.get('test_files', 0)}")
    print(f"   • Avg Function Length: {quality.get('avg_function_length', 0)} lines")
    
    # Example 5: Health score breakdown
    print("\n5️⃣  Repository Health Score:")
    health_score = results.get("summary", {}).get("health_score", 0)
    print(f"   Overall Score: {health_score}/100")
    
    if health_score >= 90:
        rating = "Excellent ⭐⭐⭐⭐⭐"
    elif health_score >= 80:
        rating = "Good ⭐⭐⭐⭐"
    elif health_score >= 70:
        rating = "Fair ⭐⭐⭐"
    elif health_score >= 60:
        rating = "Needs Improvement ⭐⭐"
    else:
        rating = "Critical ⭐"
    
    print(f"   Rating: {rating}")
    
    # Example 6: Top dependencies
    print("\n6️⃣  Most Used Dependencies:")
    dependencies = results.get("dependencies", {})
    common_packages = dependencies.get("common_packages", {})
    top_deps = sorted(common_packages.items(), key=lambda x: x[1], reverse=True)[:5]
    for pkg, count in top_deps:
        print(f"   • {pkg:25} (used in {count} services)")
    
    # Example 7: Generate custom report
    print("\n7️⃣  Generating Reports...")
    analyzer.generate_report("CODEBASE_ANALYSIS.md")
    analyzer.save_json("codebase_analysis.json")
    print("   ✓ Markdown report: CODEBASE_ANALYSIS.md")
    print("   ✓ JSON data: codebase_analysis.json")
    
    # Example 8: Access raw data for custom processing
    print("\n8️⃣  Raw Data Access:")
    print(f"   Available result keys: {list(results.keys())}")
    print(f"   Total data points: {len(str(results))} characters")
    
    print("\n" + "=" * 70)
    print("Example completed successfully!")
    print("=" * 70)
    print()
    
    return results


if __name__ == "__main__":
    main()
