# Backend API Screenshots

This directory contains screenshots of the VetrAI platform's backend API documentation.

## API Documentation Screenshots

All backend services expose Swagger UI documentation at their `/docs` endpoint.

Screenshots to capture:

### Core Services
1. `api-auth.png` - Authentication Service (Port 8001)
2. `api-tenancy.png` - Tenancy Service (Port 8002)
3. `api-keys.png` - API Keys Service (Port 8003)
4. `api-billing.png` - Billing Service (Port 8004)
5. `api-support.png` - Support Service (Port 8005)
6. `api-themes.png` - Themes Service (Port 8006)
7. `api-notifications.png` - Notifications Service (Port 8007)
8. `api-workers.png` - Workers Service (Port 8008)

### Monitoring
9. `grafana-dashboard.png` - Grafana Dashboard (Port 3002)
10. `prometheus-metrics.png` - Prometheus Metrics (Port 9090)

## Capturing API Documentation Screenshots

1. **Start all services:**
   ```bash
   docker compose up -d
   ```

2. **Wait for services to be ready:**
   ```bash
   # Check service health
   curl http://localhost:8001/health
   curl http://localhost:8002/health
   # ... etc
   ```

3. **Access Swagger UI for each service:**
   - Auth Service: http://localhost:8001/docs
   - Tenancy Service: http://localhost:8002/docs
   - Keys Service: http://localhost:8003/docs
   - Billing Service: http://localhost:8004/docs
   - Support Service: http://localhost:8005/docs
   - Themes Service: http://localhost:8006/docs
   - Notifications Service: http://localhost:8007/docs
   - Workers Service: http://localhost:8008/docs

4. **Capture screenshots** showing:
   - The service name and version
   - List of available endpoints
   - At least one expanded endpoint showing request/response schemas
   - Authorization section if applicable

## Screenshot Content Guidelines

### What to Show
- Service title and API version
- Endpoint categories/tags
- Key endpoints (expanded)
- Request/response models
- Example values
- Authentication requirements

### What to Hide/Avoid
- Real API keys or tokens
- Sensitive configuration values
- Personal information
- Production URLs or credentials

## Image Guidelines

- **Format**: PNG preferred
- **Resolution**: Full width, capture full page or key sections
- **File size**: Keep under 500KB (optimize if needed)
- **Naming**: Use lowercase with hyphens (e.g., `api-auth.png`)
- **Browser**: Use Chrome/Chromium for consistent rendering

## Swagger UI Features to Highlight

- Interactive "Try it out" buttons
- Schema definitions
- Response examples
- HTTP status codes
- Authentication/Authorization info

## Automation Script Example

```python
# screenshot_apis.py
import requests
from playwright.sync_api import sync_playwright

services = [
    ("auth", 8001),
    ("tenancy", 8002),
    ("keys", 8003),
    ("billing", 8004),
    ("support", 8005),
    ("themes", 8006),
    ("notifications", 8007),
    ("workers", 8008),
]

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    
    for name, port in services:
        page.goto(f"http://localhost:{port}/docs")
        page.screenshot(path=f"docs/screenshots/backend/api-{name}.png")
    
    browser.close()
```

## Verification

After capturing screenshots, verify:
- [ ] All images are present
- [ ] Images are properly named
- [ ] No sensitive data is visible
- [ ] Images are clear and readable
- [ ] File sizes are reasonable
