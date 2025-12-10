#!/usr/bin/env python3
"""Fix Docker health checks by replacing curl with python"""

import re

# Read the current docker-compose.backend.yml
with open('docker-compose.backend.yml', 'r') as f:
    content = f.read()

# Replace all curl health check commands with python equivalents
new_content = re.sub(
    r'test: \["CMD", "curl", "-f", "http://localhost:8000/health"\]',
    'test: ["CMD", "python", "-c", "import urllib.request; urllib.request.urlopen(\'http://localhost:8000/health\')"]',
    content
)

# Write the updated content back
with open('docker-compose.backend.yml', 'w') as f:
    f.write(new_content)

print("✅ Updated all health checks to use Python instead of curl")
print("🔄 Health checks will now work properly with the containers")