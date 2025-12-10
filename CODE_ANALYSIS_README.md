# VetrAI Code Analysis Tool

## Overview

This directory contains a comprehensive code analysis tool (`analyze_codebase.py`) that provides detailed insights into the VetrAI repository structure, code quality, security, and documentation.

## Quick Start

### Run Basic Analysis

```bash
python3 analyze_codebase.py
```

This will generate a `CODEBASE_ANALYSIS.md` report in the current directory.

### Run with JSON Output

```bash
python3 analyze_codebase.py --json
```

This generates both the Markdown report and a `codebase_analysis.json` file with structured data.

### Specify Custom Path and Output

```bash
python3 analyze_codebase.py --path /path/to/repo --output my_report.md --json
```

## Features

The analysis tool provides comprehensive insights across multiple dimensions:

### 1. **Code Metrics** 📊
- Total file counts by type (Python, JavaScript, Markdown, YAML, etc.)
- Lines of code analysis (code, comments, blank lines)
- Directory structure overview
- File size distribution

### 2. **Service Architecture** 🏗️
- Microservices discovery and analysis
- Port assignments
- API endpoint extraction
- Database model identification
- Docker and requirements.txt verification
- Test coverage status

### 3. **Dependency Analysis** 📦
- Common packages used across services
- Version tracking
- Potential version conflicts
- Service-specific dependencies

### 4. **Documentation Coverage** 📚
- Markdown file inventory
- README and CONTRIBUTING checks
- API, architecture, and deployment documentation verification
- Total documentation line count

### 5. **Security Analysis** 🔒
- Security file verification (.env.example, .gitignore, SECURITY.md)
- JWT authentication detection
- Password hashing verification
- Hardcoded secret scanning
- Security pattern identification

### 6. **Code Quality** ✨
- Module docstring coverage
- Type hint usage
- Test file count
- Average function length
- Long file identification (>500 lines)

### 7. **Health Score** 💯
- Overall repository health score (0-100)
- Based on documentation, security, services, and code quality
- Actionable recommendations

## Output Files

### Markdown Report (`CODEBASE_ANALYSIS.md`)
A comprehensive, human-readable report with:
- Executive summary
- Detailed metrics for all analysis categories
- Service-by-service breakdown
- Endpoint listings
- Recommendations for improvement

### JSON Data (`codebase_analysis.json`)
Structured data export suitable for:
- CI/CD integration
- Automated quality gates
- Trend analysis
- Custom reporting

## Usage Examples

### 1. CI/CD Integration

```yaml
# .github/workflows/code-analysis.yml
name: Code Analysis

on: [push, pull_request]

jobs:
  analyze:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run Code Analysis
        run: python3 analyze_codebase.py --json
      - name: Upload Reports
        uses: actions/upload-artifact@v2
        with:
          name: analysis-reports
          path: |
            CODEBASE_ANALYSIS.md
            codebase_analysis.json
```

### 2. Quality Gate Check

```bash
#!/bin/bash
# check_quality.sh

python3 analyze_codebase.py --json

# Extract health score from JSON
HEALTH_SCORE=$(python3 -c "import json; print(json.load(open('codebase_analysis.json'))['summary']['health_score'])")

if [ "$HEALTH_SCORE" -lt 80 ]; then
    echo "Health score $HEALTH_SCORE is below threshold (80)"
    exit 1
fi

echo "Health score $HEALTH_SCORE passes quality gate"
```

### 3. Regular Reporting

```bash
#!/bin/bash
# weekly_analysis.sh

DATE=$(date +%Y-%m-%d)
python3 analyze_codebase.py --output "reports/analysis_${DATE}.md" --json

# Commit to repository
git add reports/
git commit -m "Weekly code analysis: ${DATE}"
git push
```

## Command-Line Options

```
usage: analyze_codebase.py [-h] [--path PATH] [--output OUTPUT] [--json] [--verbose]

Analyze VetrAI codebase

optional arguments:
  -h, --help       show this help message and exit
  --path PATH      Repository path (default: current directory)
  --output OUTPUT  Output report filename (default: CODEBASE_ANALYSIS.md)
  --json           Also save results as JSON
  --verbose        Verbose output
```

## Understanding the Health Score

The health score (0-100) is calculated based on:

- **Documentation (25%)**: README, CONTRIBUTING, API docs, architecture, deployment
- **Security (25%)**: Security files, JWT usage, password hashing
- **Services (25%)**: Dockerfiles, requirements.txt, test coverage
- **Code Quality (25%)**: Docstrings, type hints, test files

### Score Interpretation

- **90-100**: Excellent - Well-maintained codebase
- **80-89**: Good - Minor improvements needed
- **70-79**: Fair - Some attention required
- **60-69**: Needs Improvement - Multiple areas to address
- **<60**: Critical - Significant work needed

## Recommendations Section

Each analysis includes actionable recommendations based on findings:

- Missing documentation
- Services without Dockerfiles
- Services without tests
- Low docstring coverage
- Security concerns
- And more...

## Extending the Analysis

### Adding New Metrics

To add custom analysis metrics, extend the `CodeAnalyzer` class:

```python
def analyze_custom_metric(self):
    """Add your custom analysis here"""
    self.results["custom"] = {
        # Your metrics
    }

# Add to analyze() method
def analyze(self):
    # ... existing code ...
    self.analyze_custom_metric()
    # ... existing code ...
```

### Custom Reports

Modify the `generate_report()` method to customize output format:

```python
def generate_report(self, output_file: str = "CODEBASE_ANALYSIS.md"):
    report = []
    # Add your custom sections
    report.append("## My Custom Section\n")
    # ...
```

## Technical Details

### File Exclusions

The analyzer automatically excludes:
- `.git` directory
- `node_modules`
- `venv` and `.venv` (Python virtual environments)
- `__pycache__`
- `dist` and `build` directories
- `.github` directory

### Pattern Matching

Uses regex patterns to identify:
- FastAPI route decorators
- SQLAlchemy model definitions
- Security patterns (JWT, bcrypt)
- Hardcoded credentials
- Type hints and docstrings

### Performance

- Typical analysis time: 5-10 seconds for medium repositories
- Memory efficient: Processes files one at a time
- No external API calls required

## Troubleshooting

### Issue: Permission Denied

```bash
chmod +x analyze_codebase.py
```

### Issue: Module Not Found

The script uses only Python standard library modules. No additional dependencies required.

### Issue: Encoding Errors

The script uses `errors='ignore'` for file reading to handle various encodings gracefully.

## Best Practices

1. **Run Regularly**: Execute analysis weekly or on major changes
2. **Track Trends**: Compare health scores over time
3. **Set Baselines**: Define minimum acceptable scores for your team
4. **Automate**: Integrate into CI/CD pipeline
5. **Act on Recommendations**: Address findings systematically

## Contributing

To improve the analysis tool:

1. Fork the repository
2. Add your enhancements to `analyze_codebase.py`
3. Test thoroughly on diverse repositories
4. Submit a pull request with examples

## License

Same as the VetrAI project - MIT License

## Support

For issues or questions:
- Open an issue on GitHub
- Contact: support@vetrai.io
- Documentation: See main README.md

---

**Last Updated**: December 2024
**Version**: 1.0.0
