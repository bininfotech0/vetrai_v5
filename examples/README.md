# VetrAI Code Analysis - Usage Examples

This directory contains practical examples of using the VetrAI code analysis tool in different scenarios.

## 📁 Files

### 1. `analyze_example.py`
**Programmatic Usage Example**

Demonstrates how to use the `CodeAnalyzer` class programmatically from Python code.

```bash
python3 analyze_example.py
```

**What it shows:**
- Importing and initializing the analyzer
- Running analysis and accessing results
- Extracting specific metrics (services, documentation, security, quality)
- Generating custom reports
- Working with the JSON output

**Use cases:**
- Building custom analysis dashboards
- Integrating into Python applications
- Creating specialized reports
- Automating code quality tracking

---

### 2. `ci_quality_gate.sh`
**CI/CD Quality Gate Example**

A bash script that demonstrates how to enforce code quality standards in CI/CD pipelines.

```bash
# Basic usage
./ci_quality_gate.sh

# With custom threshold
./ci_quality_gate.sh --health-threshold 85

# Strict mode (fail on any potential secrets)
./ci_quality_gate.sh --health-threshold 90 --fail-on-secrets
```

**Quality Gates Checked:**
1. ✅ Health score threshold (default: 80/100)
2. ✅ No hardcoded secrets (warning by default, fail with `--fail-on-secrets`)
3. ✅ Required documentation (README, CONTRIBUTING, API docs)
4. ✅ Security patterns (JWT, password hashing, .env.example)

**Exit Codes:**
- `0`: All quality gates passed
- `1`: One or more quality gates failed

**Use cases:**
- GitHub Actions workflows
- GitLab CI/CD pipelines
- Jenkins jobs
- Pre-commit hooks
- Automated deployment gates

---

## 🚀 Quick Start

### Run All Examples

```bash
# Programmatic usage
cd /path/to/vetrai_v5
python3 examples/analyze_example.py

# CI/CD quality gate
bash examples/ci_quality_gate.sh
```

### GitHub Actions Integration

```yaml
# .github/workflows/code-quality.yml
name: Code Quality Gate

on: [push, pull_request]

jobs:
  analyze:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Run Quality Gate
        run: |
          chmod +x examples/ci_quality_gate.sh
          bash examples/ci_quality_gate.sh --health-threshold 85
      
      - name: Upload Analysis Report
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: code-analysis
          path: |
            CODEBASE_ANALYSIS.md
            codebase_analysis.json
```

### GitLab CI Integration

```yaml
# .gitlab-ci.yml
code_analysis:
  stage: test
  image: python:3.11
  script:
    - chmod +x examples/ci_quality_gate.sh
    - bash examples/ci_quality_gate.sh --health-threshold 80
  artifacts:
    when: always
    paths:
      - CODEBASE_ANALYSIS.md
      - codebase_analysis.json
    reports:
      junit: analysis-report.xml
```

### Jenkins Integration

```groovy
// Jenkinsfile
pipeline {
    agent any
    
    stages {
        stage('Code Analysis') {
            steps {
                sh 'python3 analyze_codebase.py --json'
            }
        }
        
        stage('Quality Gate') {
            steps {
                script {
                    def exitCode = sh(
                        script: 'bash examples/ci_quality_gate.sh --health-threshold 85',
                        returnStatus: true
                    )
                    if (exitCode != 0) {
                        error("Quality gate failed!")
                    }
                }
            }
        }
    }
    
    post {
        always {
            archiveArtifacts artifacts: 'CODEBASE_ANALYSIS.md,codebase_analysis.json'
        }
    }
}
```

---

## 💡 Advanced Usage Examples

### Custom Quality Gate Thresholds

```bash
# Set via environment variables
export HEALTH_THRESHOLD=85
export FAIL_ON_SECRETS=true

bash examples/ci_quality_gate.sh
```

### Extract Specific Metrics

```python
import json

with open('codebase_analysis.json') as f:
    data = json.load(f)

# Get health score
health = data['summary']['health_score']

# Get service count
services = len(data['services'])

# Get documentation status
has_readme = data['documentation']['readme_found']

# Get security info
uses_jwt = data['security']['security_patterns']['jwt_usage']

print(f"Health: {health}/100")
print(f"Services: {services}")
print(f"README: {has_readme}")
print(f"JWT: {uses_jwt}")
```

### Track Quality Over Time

```bash
#!/bin/bash
# track_quality.sh - Track code quality metrics over time

DATE=$(date +%Y-%m-%d)
LOG_DIR="quality_logs"

mkdir -p "$LOG_DIR"

# Run analysis
python3 analyze_codebase.py --json

# Extract health score
HEALTH=$(python3 -c "import json; print(json.load(open('codebase_analysis.json'))['summary']['health_score'])")

# Log to CSV
echo "${DATE},${HEALTH}" >> "${LOG_DIR}/health_history.csv"

# Archive full report
cp codebase_analysis.json "${LOG_DIR}/analysis_${DATE}.json"

echo "Health score: ${HEALTH}/100 (logged to ${LOG_DIR}/health_history.csv)"
```

### Pre-commit Hook

```bash
#!/bin/bash
# .git/hooks/pre-commit

echo "Running code analysis..."
python3 analyze_codebase.py --json > /dev/null 2>&1

HEALTH=$(python3 -c "import json; print(json.load(open('codebase_analysis.json'))['summary']['health_score'])")

if [ "$HEALTH" -lt 70 ]; then
    echo "❌ Commit blocked: Health score ${HEALTH} is below 70"
    echo "Run 'python3 analyze_codebase.py' to see the full report"
    exit 1
fi

echo "✓ Health score: ${HEALTH}/100"
```

---

## 📊 Monitoring and Reporting

### Generate Trend Report

```python
# trend_analysis.py
import json
import glob
from pathlib import Path
import matplotlib.pyplot as plt

# Load historical data
quality_logs = sorted(glob.glob('quality_logs/analysis_*.json'))

dates = []
health_scores = []
lines_of_code = []

for log_file in quality_logs:
    with open(log_file) as f:
        data = json.load(f)
        date = Path(log_file).stem.replace('analysis_', '')
        dates.append(date)
        health_scores.append(data['summary']['health_score'])
        lines_of_code.append(data['summary']['total_code_lines'])

# Plot trends
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

ax1.plot(dates, health_scores, marker='o')
ax1.set_ylabel('Health Score')
ax1.set_title('Code Quality Trend')
ax1.grid(True)

ax2.plot(dates, lines_of_code, marker='s', color='green')
ax2.set_ylabel('Lines of Code')
ax2.set_xlabel('Date')
ax2.grid(True)

plt.tight_layout()
plt.savefig('quality_trends.png')
print("Trend report saved to quality_trends.png")
```

---

## 🔧 Customization

### Add Custom Quality Gates

Edit `ci_quality_gate.sh` to add your own checks:

```bash
# Gate: Minimum test coverage
TEST_FILES=$(python3 -c "
import json
with open('codebase_analysis.json') as f:
    print(json.load(f)['quality']['test_files'])
")

if [ "$TEST_FILES" -lt 10 ]; then
    echo "❌ FAIL: Only ${TEST_FILES} test files found (minimum: 10)"
    EXIT_CODE=1
fi
```

### Integrate with Slack/Discord

```bash
# Send results to Slack
WEBHOOK_URL="your-slack-webhook-url"

python3 analyze_codebase.py --json

HEALTH=$(python3 -c "import json; print(json.load(open('codebase_analysis.json'))['summary']['health_score'])")

MESSAGE="Code Analysis Complete\nHealth Score: ${HEALTH}/100"

curl -X POST "$WEBHOOK_URL" \
    -H 'Content-Type: application/json' \
    -d "{\"text\":\"${MESSAGE}\"}"
```

---

## 📚 Additional Resources

- **Main Documentation**: See `CODE_ANALYSIS_README.md` in the root directory
- **Full Analysis Tool**: `analyze_codebase.py` in the root directory
- **Generated Reports**: Look for `CODEBASE_ANALYSIS.md` and `codebase_analysis.json`

---

## 🤝 Contributing

Have a useful example? Contribute it!

1. Create your example script/file
2. Test it thoroughly
3. Add documentation here
4. Submit a pull request

---

**Last Updated**: December 2024
