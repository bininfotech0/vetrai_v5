# Frontend Screenshots

This directory contains screenshots of the VetrAI platform's frontend interfaces.

## Studio Interface (Port 3000)

Screenshots to capture:
1. `studio-dashboard.png` - Main dashboard view
2. `studio-workflow-builder.png` - Workflow visual editor
3. `studio-execution.png` - Workflow execution view

## Admin Dashboard (Port 3001)

Screenshots to capture:
1. `admin-dashboard.png` - Main admin overview
2. `admin-organizations.png` - Organization management
3. `admin-users.png` - User management
4. `admin-api-keys.png` - API keys interface
5. `admin-billing.png` - Billing dashboard
6. `admin-support.png` - Support ticketing system
7. `admin-themes.png` - Theme customization
8. `admin-notifications.png` - Notifications center

## Capturing Screenshots

### Option 1: Manual Screenshots
1. Start the platform: `docker compose up -d`
2. Navigate to http://localhost:3000 (Studio) or http://localhost:3001 (Admin)
3. Use your browser's screenshot tool or OS screenshot utility
4. Save images here with the filenames listed above

### Option 2: Automated Screenshots (Using Playwright)
```bash
# Install Playwright
npm install -D @playwright/test
npx playwright install

# Create a screenshot script or use browser automation
```

### Option 3: Using Browser DevTools
1. Open browser DevTools (F12)
2. Use device emulation for consistent sizes
3. Take screenshots with browser screenshot feature

## Image Guidelines

- **Format**: PNG preferred (supports transparency)
- **Resolution**: 1920x1080 or higher for desktop views
- **File size**: Keep under 500KB per image (optimize if needed)
- **Naming**: Use lowercase with hyphens (kebab-case)
- **Content**: Ensure no sensitive data is visible (use demo/sample data)

## Demo Data

Before capturing screenshots, seed the database with demo data:
```bash
./scripts/seeding/seed_dev.sh
```

This will create sample organizations, users, workflows, etc. for better screenshots.
