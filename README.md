# VetrAI Platform

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109.1-00C7B7.svg)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg)](https://www.docker.com/)
[![Security](https://img.shields.io/badge/security-patched-green.svg)](https://github.com/bininfotech0/vetrai_v5/security)

VetrAI is a commercial-grade AI workflow platform built on top of LangFlow, featuring enterprise capabilities including multi-tenancy, advanced authentication, billing integration, and comprehensive API management.

> **✅ Platform Complete**: All 8 microservices are now implemented and fully integrated. See [SERVICES.md](docs/SERVICES.md) for detailed service documentation.

## 🚀 Features

### Core Platform
- **🔐 Multi-Tenant Architecture**: Complete organization and tenant management with data isolation
- **👥 Advanced Authentication**: JWT-based auth with RBAC, supporting multiple roles
- **🔑 API Key Management**: Secure API key generation with scoped permissions and rate limiting
- **💳 Billing & Subscriptions**: Stripe integration with usage-based billing
- **🎫 Support System**: Complete ticketing system with SLA management
- **🎨 Theming & Branding**: Dynamic themes and branding per organization
- **📧 Notifications**: Multi-channel notifications (Email, SMS, In-app)
- **⚙️ LangGraph Integration**: Advanced workflow execution with job queues

### Technical Stack
- **Backend**: FastAPI (Python 3.11+)
- **Database**: PostgreSQL with pgvector
- **Cache/Queue**: Redis
- **Storage**: MinIO (S3-compatible)
- **Frontend**: React/TypeScript
- **Payments**: Stripe, Razorpay (optional)
- **Monitoring**: Prometheus + Grafana
- **Deployment**: Docker, Kubernetes

## 📋 Table of Contents

- [Quick Start](#quick-start)
- [Screenshots](#screenshots)
- [Architecture](#architecture)
- [Services](#services)
- [Development Setup](#development-setup)
- [Deployment](#deployment)
- [API Documentation](#api-documentation)
- [Contributing](#contributing)
- [License](#license)

## 🏃 Quick Start

### Prerequisites

- Docker & Docker Compose
- Python 3.11+
- Node.js 18+
- PostgreSQL 15+
- Redis 7+

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/bininfotech0/vetrai_v5.git
   cd vetrai_v5
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configurations
   ```

3. **Start services with Docker Compose**
   ```bash
   docker-compose up -d
   ```

4. **Run database migrations**
   ```bash
   ./scripts/setup/migrate.sh
   ```

5. **Seed initial data (optional)**
   ```bash
   ./scripts/seeding/seed_dev.sh
   ```

6. **Access the platform**
   - Studio: http://localhost:3000
   - Admin Dashboard: http://localhost:3001
   - API Documentation: http://localhost:8000/docs

## 📸 Screenshots

Visual overview of the VetrAI platform's frontend and backend interfaces:

### Frontend
- **Studio Dashboard**: Visual workflow builder with LangFlow integration
- **Admin Dashboard**: Comprehensive management interface for the entire platform

### Backend
- **API Documentation**: Interactive Swagger UI for all 8 microservices
- **Monitoring**: Grafana and Prometheus dashboards

👉 **[View all screenshots and detailed documentation](docs/SCREENSHOTS.md)**

## 🏗️ Architecture

VetrAI follows a microservices architecture with the following components:

```
┌─────────────────────────────────────────────────────────────┐
│                        Load Balancer                         │
└─────────────────────────────────────────────────────────────┘
                              │
         ┌────────────────────┼────────────────────┐
         │                    │                    │
    ┌────▼─────┐        ┌────▼─────┐        ┌────▼─────┐
    │  Studio  │        │  Admin   │        │  Public  │
    │ Frontend │        │Dashboard │        │ Website  │
    └────┬─────┘        └────┬─────┘        └────┬─────┘
         │                   │                    │
         └───────────────────┼────────────────────┘
                             │
                    ┌────────▼─────────┐
                    │   API Gateway    │
                    └────────┬─────────┘
                             │
         ┌───────────────────┼───────────────────┐
         │                   │                   │
    ┌────▼─────┐      ┌─────▼──────┐     ┌─────▼──────┐
    │   Auth   │      │  Tenancy   │     │    Keys    │
    │ Service  │      │  Service   │     │  Service   │
    └──────────┘      └────────────┘     └────────────┘
         │                   │                   │
    ┌────▼─────┐      ┌─────▼──────┐     ┌─────▼──────┐
    │ Billing  │      │  Support   │     │   Themes   │
    │ Service  │      │  Service   │     │  Service   │
    └──────────┘      └────────────┘     └────────────┘
         │                   │                   │
    ┌────▼─────┐      ┌─────▼──────┐
    │Notification│     │  Workers   │
    │  Service  │     │  Service   │
    └───────────┘     └────────────┘
         │                   │
         └───────────────────┼───────────────────┘
                             │
         ┌───────────────────┼───────────────────┐
         │                   │                   │
    ┌────▼─────┐      ┌─────▼──────┐     ┌─────▼──────┐
    │PostgreSQL│      │   Redis    │     │   MinIO    │
    └──────────┘      └────────────┘     └────────────┘
```

## 🔧 Services

All 8 microservices are fully implemented and documented. See [SERVICES.md](docs/SERVICES.md) for complete API documentation.

### 1. Authentication Service (Port 8001)
JWT + opaque token authentication with refresh tokens, password reset, email verification, and RBAC with 5 roles: `super_admin`, `org_admin`, `user`, `support_agent`, `billing_admin`.

**Key Endpoints**: `/api/v1/register`, `/api/v1/login`, `/api/v1/refresh`, `/api/v1/me`, `/api/v1/users`

### 2. Tenancy Service (Port 8002)
Multi-tenant architecture with organization management, plan assignment, and complete tenant data isolation.

**Key Endpoints**: `/api/v1/organizations` (CRUD operations)

### 3. API Keys Service (Port 8003)
Secure API key generation with scoped permissions, rate limiting configuration, and comprehensive usage tracking.

**Key Endpoints**: `/api/v1/keys`, `/api/v1/keys/{id}/usage`

### 4. Billing Service (Port 8004)
Full Stripe integration for payments, subscription management, webhook handling, invoice generation, and usage-based billing.

**Key Endpoints**: `/api/v1/billing/subscriptions`, `/api/v1/billing/invoices`, `/api/v1/billing/webhooks/stripe`

### 5. Support Service (Port 8005)
Complete ticketing system with file attachments (MinIO), comment threads, ticket assignment, and priority management.

**Key Endpoints**: `/api/v1/support/tickets`, `/api/v1/support/tickets/{id}/comments`, `/api/v1/support/tickets/{id}/attachments`

### 6. Themes Service (Port 8006)
Dynamic theme management with custom colors, logo/favicon uploads, custom CSS injection, and public page content management.

**Key Endpoints**: `/api/v1/themes`, `/api/v1/themes/pages`

### 7. Notifications Service (Port 8007)
Multi-channel notifications (Email, SMS, In-app, Push) with reusable templates and Redis-based delivery queues.

**Key Endpoints**: `/api/v1/notifications`, `/api/v1/notifications/templates`

### 8. Workers Service (Port 8008)
LangGraph workflow execution with Celery job queues, workflow templates, job status tracking, and retry logic.

**Key Endpoints**: `/api/v1/workers/jobs`, `/api/v1/workers/templates`

## 💻 Development Setup

### Backend Services

Each service follows the same structure:

```
services/<service-name>/
├── app/
│   ├── main.py           # FastAPI application
│   ├── models.py         # SQLAlchemy models
│   ├── schemas.py        # Pydantic schemas
│   ├── routes.py         # API endpoints
│   ├── dependencies.py   # Dependency injection
│   └── config.py         # Service configuration
├── tests/
├── requirements.txt
└── Dockerfile
```

To run a service locally:

```bash
cd services/<service-name>
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### Frontend Applications

```bash
cd frontend/<app-name>
npm install
npm run dev
```

## 🚢 Deployment

### Docker Compose (Development)

```bash
docker-compose -f infra/docker/docker-compose.yml up -d
```

### Kubernetes (Production)

```bash
# Install Helm charts
helm install vetrai infra/k8s/vetrai-platform \
  --namespace vetrai \
  --create-namespace \
  --values infra/k8s/values-production.yaml
```

### Terraform (Infrastructure)

```bash
cd infra/terraform
terraform init
terraform plan
terraform apply
```

## 📚 API Documentation

API documentation is available at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- OpenAPI JSON: http://localhost:8000/openapi.json

## 🧪 Testing

```bash
# Run all tests
pytest

# Run specific service tests
pytest services/auth/tests/

# Run integration tests
pytest tests/integration/

# Run with coverage
pytest --cov=services --cov-report=html
```

## 🔒 Security

- **All Security Patches Applied**: Dependencies updated to latest secure versions
- TLS/SSL enforced in production
- Secrets managed via environment variables and Kubernetes secrets
- RBAC enforcement across all services
- Rate limiting on all API endpoints
- Audit logging for sensitive operations
- GDPR compliance features
- Data encryption at rest and in transit

**Security Policy**: See [SECURITY.md](SECURITY.md) for vulnerability reporting and security updates.

## 📖 Documentation

Detailed documentation is available in the `/docs` directory:

- [Screenshots & Visual Guide](docs/SCREENSHOTS.md)
- [API Documentation](docs/api/README.md)
- [Architecture Guide](docs/architecture/README.md)
- [Deployment Guide](docs/deployment/README.md)
- [Development Guide](docs/guides/development.md)
- [Security Guide](docs/guides/security.md)

## 🤝 Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built on top of [LangFlow](https://github.com/logspace-ai/langflow)
- Powered by [FastAPI](https://fastapi.tiangolo.com/)
- Inspired by enterprise AI workflow platforms

## 📞 Support

- Documentation: [docs.vetrai.io](https://docs.vetrai.io)
- Issue Tracker: [GitHub Issues](https://github.com/bininfotech0/vetrai_v5/issues)
- Email: support@vetrai.io
- Community: [Discord](https://discord.gg/vetrai)

## 🗺️ Roadmap

- [ ] Advanced workflow templates
- [ ] AI model marketplace
- [ ] Enhanced analytics dashboard
- [ ] Mobile applications
- [ ] Enterprise SSO integration
- [ ] Advanced audit logging
- [ ] Multi-region deployment
- [ ] Custom model training

---

**Made with ❤️ by the VetrAI Team**