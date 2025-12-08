# Security Policy

## Supported Versions

We actively maintain and provide security updates for the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Security Updates

### Latest Security Patches (December 2024)

All dependencies have been updated to address known vulnerabilities:

#### FastAPI Security Update
- **Previous Version**: 0.104.1
- **Updated To**: 0.109.1
- **CVE**: Content-Type Header ReDoS vulnerability
- **Severity**: Medium
- **Status**: ✅ Patched

#### python-multipart Security Updates
- **Previous Version**: 0.0.6
- **Updated To**: 0.0.18
- **Vulnerabilities Fixed**:
  1. Denial of Service (DoS) via malformed multipart/form-data boundary
  2. Content-Type Header ReDoS vulnerability
- **Severity**: High
- **Status**: ✅ Patched

#### aiohttp Security Updates
- **Previous Version**: 3.9.1
- **Updated To**: 3.9.4
- **Vulnerabilities Fixed**:
  1. Denial of Service when parsing malformed POST requests
  2. Directory traversal vulnerability
- **Severity**: High
- **Status**: ✅ Patched

## Reporting a Vulnerability

We take security seriously. If you discover a security vulnerability in VetrAI Platform, please follow these steps:

### 1. Do NOT Create a Public Issue

Please **do not** report security vulnerabilities through public GitHub issues, discussions, or pull requests.

### 2. Report Privately

Send a detailed report to: **security@vetrai.io**

Include:
- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)
- Your contact information

### 3. Response Timeline

- **Initial Response**: Within 24-48 hours
- **Status Update**: Within 5 business days
- **Fix Timeline**: Critical issues within 7 days, others within 30 days

### 4. Disclosure Policy

- We will acknowledge your report within 48 hours
- We will keep you informed of the progress
- We will credit you in the security advisory (unless you prefer to remain anonymous)
- We request that you do not publicly disclose the vulnerability until we have released a fix

## Security Best Practices

### For Developers

1. **Never commit secrets**
   ```bash
   # Use .env files (already in .gitignore)
   cp .env.example .env
   # Edit .env with your secrets
   ```

2. **Keep dependencies updated**
   ```bash
   pip install --upgrade -r requirements.txt
   ```

3. **Run security scans**
   ```bash
   # Bandit for Python security issues
   bandit -r services/
   
   # Safety for dependency vulnerabilities
   safety check
   ```

4. **Use pre-commit hooks**
   ```bash
   pip install pre-commit
   pre-commit install
   ```

### For Deployment

1. **Use strong secrets**
   ```bash
   # Generate secure keys
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```

2. **Enable HTTPS/TLS**
   - Use Let's Encrypt certificates
   - Enforce SSL redirects
   - Set secure cookie flags

3. **Database security**
   - Use strong passwords
   - Enable SSL connections
   - Restrict network access
   - Regular backups

4. **Environment isolation**
   - Separate dev/staging/production
   - Use different credentials per environment
   - Network segmentation

5. **Monitoring & Logging**
   - Enable audit logging
   - Monitor for suspicious activity
   - Set up alerts for security events

## Security Features

### Authentication & Authorization

- **JWT Tokens**: Short-lived access tokens (30 min) with refresh tokens (7 days)
- **Password Security**: Bcrypt hashing with salt
- **RBAC**: Role-based access control with 5 role types
- **Token Revocation**: Refresh tokens can be revoked
- **Audit Logging**: All sensitive operations are logged

### Data Protection

- **Multi-Tenancy**: Strict data isolation per organization
- **Encryption**: 
  - Passwords hashed with bcrypt
  - API keys hashed before storage
  - TLS/SSL for data in transit
- **Input Validation**: Pydantic schemas for all API inputs
- **SQL Injection Prevention**: Parameterized queries via SQLAlchemy

### API Security

- **Rate Limiting**: Configurable per user/API key
- **CORS**: Configurable allowed origins
- **API Keys**: Scoped permissions per key
- **Request Validation**: Comprehensive input validation

### Infrastructure Security

- **Docker**: Non-root users in containers
- **Network**: Isolated Docker networks
- **Secrets Management**: Environment variables, never hardcoded
- **Health Checks**: Regular service health monitoring

## Security Checklist for Production

- [ ] All secrets are stored securely (environment variables/secrets manager)
- [ ] HTTPS/TLS is enabled with valid certificates
- [ ] Database connections use SSL
- [ ] Strong passwords for all accounts
- [ ] Rate limiting is enabled
- [ ] CORS is properly configured
- [ ] Audit logging is enabled
- [ ] Regular security updates are applied
- [ ] Backups are configured and tested
- [ ] Monitoring and alerts are set up
- [ ] Firewall rules are configured
- [ ] Regular security scans are performed

## Dependency Management

We regularly monitor and update dependencies for security vulnerabilities:

### Automated Scanning

- **GitHub Dependabot**: Automatic dependency updates
- **CI/CD Pipeline**: Security scanning on every commit
- **Safety**: Python dependency vulnerability checks

### Update Schedule

- **Critical**: Immediate (within 24 hours)
- **High**: Within 1 week
- **Medium**: Within 1 month
- **Low**: Next regular update cycle

## Compliance

VetrAI is designed with compliance in mind:

- **GDPR**: Data export, deletion, and privacy controls
- **SOC 2**: Audit logging and access controls
- **ISO 27001**: Security best practices implemented
- **OWASP Top 10**: Protection against common vulnerabilities

## Security Contact

- **Email**: security@vetrai.io
- **PGP Key**: [Available on request]
- **Bug Bounty**: Coming soon

## Acknowledgments

We appreciate the security researchers who help keep VetrAI secure. Thank you to all who responsibly disclose vulnerabilities.

---

**Last Updated**: December 2024
**Next Review**: January 2025
