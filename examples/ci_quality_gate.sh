#!/bin/bash
# CI/CD Quality Gate Example
# 
# This script demonstrates how to use the code analysis tool in CI/CD pipelines
# to enforce code quality standards.
#
# Usage: ./ci_quality_gate.sh [--health-threshold 80] [--fail-on-secrets]

set -e

# Default configuration
HEALTH_THRESHOLD=${HEALTH_THRESHOLD:-80}
FAIL_ON_SECRETS=${FAIL_ON_SECRETS:-false}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --health-threshold)
            HEALTH_THRESHOLD="$2"
            shift 2
            ;;
        --fail-on-secrets)
            FAIL_ON_SECRETS=true
            shift
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

echo "========================================================================"
echo "VetrAI Code Analysis - CI/CD Quality Gate"
echo "========================================================================"
echo ""
echo "Configuration:"
echo "  • Health Score Threshold: ${HEALTH_THRESHOLD}/100"
echo "  • Fail on Secrets: ${FAIL_ON_SECRETS}"
echo ""

# Run the analysis
echo "Running code analysis..."
python3 analyze_codebase.py --json > /dev/null

if [ ! -f "codebase_analysis.json" ]; then
    echo "❌ ERROR: Analysis failed - no JSON output generated"
    exit 1
fi

echo "✓ Analysis complete"
echo ""

# Extract metrics using Python
read HEALTH_SCORE SECRETS_COUNT SERVICES_COUNT CODE_LINES <<< $(python3 -c "
import json
with open('codebase_analysis.json', 'r') as f:
    data = json.load(f)
    health = data['summary']['health_score']
    secrets = len(data['security'].get('secrets_in_code', []))
    services = data['summary']['total_services']
    lines = data['summary']['total_code_lines']
    print(health, secrets, services, lines)
")

echo "Analysis Results:"
echo "  • Health Score: ${HEALTH_SCORE}/100"
echo "  • Services: ${SERVICES_COUNT}"
echo "  • Lines of Code: ${CODE_LINES}"
echo "  • Potential Secrets: ${SECRETS_COUNT}"
echo ""

# Check quality gates
EXIT_CODE=0

# Gate 1: Health Score
if [ "$HEALTH_SCORE" -lt "$HEALTH_THRESHOLD" ]; then
    echo "❌ FAIL: Health score ${HEALTH_SCORE} is below threshold ${HEALTH_THRESHOLD}"
    EXIT_CODE=1
else
    echo "✓ PASS: Health score meets threshold"
fi

# Gate 2: Secrets Detection
if [ "$FAIL_ON_SECRETS" = true ] && [ "$SECRETS_COUNT" -gt 0 ]; then
    echo "❌ FAIL: Found ${SECRETS_COUNT} potential hardcoded secrets"
    EXIT_CODE=1
elif [ "$SECRETS_COUNT" -gt 0 ]; then
    echo "⚠️  WARNING: Found ${SECRETS_COUNT} potential hardcoded secrets (not failing)"
else
    echo "✓ PASS: No hardcoded secrets detected"
fi

# Gate 3: Required Documentation
echo ""
echo "Documentation Checks:"
python3 -c "
import json
with open('codebase_analysis.json', 'r') as f:
    data = json.load(f)
    docs = data['documentation']
    
    checks = [
        ('README.md', docs.get('readme_found', False)),
        ('CONTRIBUTING.md', docs.get('contributing_found', False)),
        ('API Documentation', docs.get('api_docs', False)),
    ]
    
    all_passed = True
    for name, status in checks:
        symbol = '✓' if status else '❌'
        print(f'  {symbol} {name}')
        if not status:
            all_passed = False
    
    exit(0 if all_passed else 1)
" || EXIT_CODE=1

# Gate 4: Security Patterns
echo ""
echo "Security Checks:"
python3 -c "
import json
with open('codebase_analysis.json', 'r') as f:
    data = json.load(f)
    sec = data['security']
    patterns = sec.get('security_patterns', {})
    
    checks = [
        ('JWT Authentication', patterns.get('jwt_usage', False)),
        ('Password Hashing', patterns.get('password_hashing', False)),
        ('.env.example', sec.get('env_example_found', False)),
    ]
    
    all_passed = True
    for name, status in checks:
        symbol = '✓' if status else '❌'
        print(f'  {symbol} {name}')
        if not status:
            all_passed = False
    
    exit(0 if all_passed else 1)
" || EXIT_CODE=1

echo ""
echo "========================================================================"

if [ $EXIT_CODE -eq 0 ]; then
    echo "✅ All quality gates passed!"
    echo "========================================================================"
else
    echo "❌ Quality gates failed!"
    echo "========================================================================"
    echo ""
    echo "To view full analysis report:"
    echo "  cat CODEBASE_ANALYSIS.md"
    echo ""
    echo "To see recommendations:"
    echo "  grep -A 20 '## 💡 Recommendations' CODEBASE_ANALYSIS.md"
fi

exit $EXIT_CODE
