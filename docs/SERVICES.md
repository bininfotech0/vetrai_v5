# VetrAI Platform - Services Documentation

## Overview

VetrAI Platform consists of 8 microservices that work together to provide a complete enterprise AI workflow platform.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Load Balancer                         │
└─────────────────────────────────────────────────────────────┘
                               │
          ┌────────────────────┼────────────────────┐
          │                    │                    │
     ┌────▼─────┐        ┌────▼─────┐        ┌────▼─────┐
     │   Auth   │        │ Tenancy  │        │   Keys   │
     │ :8001    │        │  :8002   │        │  :8003   │
     └──────────┘        └──────────┘        └──────────┘
          │                    │                    │
     ┌────▼─────┐        ┌────▼─────┐        ┌────▼─────┐
     │ Billing  │        │ Support  │        │  Themes  │
     │  :8004   │        │  :8005   │        │  :8006   │
     └──────────┘        └──────────┘        └──────────┘
          │                    │                    │
     ┌────▼─────┐        ┌────▼─────┐
     │Notifications│      │ Workers  │
     │  :8007   │        │  :8008   │
     └──────────┘        └──────────┘
          │                    │
          └────────────────────┼────────────────────┘
                               │
          ┌────────────────────┼────────────────────┐
          │                    │                    │
     ┌────▼─────┐        ┌────▼─────┐        ┌────▼─────┐
     │PostgreSQL│        │  Redis   │        │  MinIO   │
     │  :5432   │        │  :6379   │        │  :9000   │
     └──────────┘        └──────────┘        └──────────┘
```

## Services

### 1. Authentication Service (Port 8001)

**Purpose**: User authentication, JWT token management, and user CRUD operations.

**Key Features**:
- User registration and login
- JWT + opaque token authentication
- Password reset and email verification
- Role-based access control (RBAC)
- Refresh token management
- Access token storage

**Models**:
- `User` - User accounts with roles
- `RefreshToken` - JWT refresh tokens
- `AccessToken` - Opaque access tokens
- `AuditLog` - Security audit logging

**API Endpoints**:
- `POST /api/v1/register` - Register new user
- `POST /api/v1/login` - User login
- `POST /api/v1/refresh` - Refresh access token
- `POST /api/v1/logout` - User logout
- `GET /api/v1/me` - Get current user
- `PUT /api/v1/me` - Update current user
- `POST /api/v1/change-password` - Change password
- `GET /api/v1/users` - List users (admin)
- `GET /api/v1/users/{id}` - Get user by ID
- `PUT /api/v1/users/{id}` - Update user
- `DELETE /api/v1/users/{id}` - Delete user

**Roles**:
- `super_admin` - Full platform access
- `org_admin` - Organization administration
- `user` - Standard user
- `support_agent` - Support access
- `billing_admin` - Billing management

---

### 2. Tenancy Service (Port 8002)

**Purpose**: Multi-tenant organization management and data isolation.

**Key Features**:
- Organization creation and management
- Plan assignment and limits
- Multi-tenant data isolation
- Organization settings

**Models**:
- `Organization` - Tenant organizations

**API Endpoints**:
- `POST /api/v1/organizations` - Create organization
- `GET /api/v1/organizations` - List organizations
- `GET /api/v1/organizations/{id}` - Get organization
- `PUT /api/v1/organizations/{id}` - Update organization
- `DELETE /api/v1/organizations/{id}` - Delete organization

---

### 3. API Keys Service (Port 8003)

**Purpose**: Secure API key generation with scoped permissions and usage tracking.

**Key Features**:
- API key generation with prefix
- Scoped permissions per key
- Rate limiting configuration
- Usage tracking and analytics
- Key expiration management

**Models**:
- `APIKey` - API key with scopes
- `APIKeyUsage` - Usage statistics

**API Endpoints**:
- `POST /api/v1/keys` - Create API key
- `GET /api/v1/keys` - List API keys
- `GET /api/v1/keys/{id}` - Get API key
- `PUT /api/v1/keys/{id}` - Update API key
- `DELETE /api/v1/keys/{id}` - Delete API key
- `GET /api/v1/keys/{id}/usage` - Get usage stats

---

### 4. Billing Service (Port 8004)

**Purpose**: Stripe integration for payments and subscription management.

**Key Features**:
- Subscription management
- Payment processing via Stripe
- Invoice generation
- Webhook handling
- Usage-based billing

**Models**:
- `Subscription` - Organization subscriptions
- `Invoice` - Billing invoices
- `Payment` - Payment records

**API Endpoints**:
- `POST /api/v1/billing/subscriptions` - Create subscription
- `GET /api/v1/billing/subscriptions` - List subscriptions
- `GET /api/v1/billing/subscriptions/{id}` - Get subscription
- `POST /api/v1/billing/subscriptions/{id}/cancel` - Cancel subscription
- `GET /api/v1/billing/invoices` - List invoices
- `GET /api/v1/billing/invoices/{id}` - Get invoice
- `GET /api/v1/billing/payments` - List payments
- `POST /api/v1/billing/webhooks/stripe` - Stripe webhook

---

### 5. Support Service (Port 8005)

**Purpose**: Complete ticketing system with file attachments and SLA management.

**Key Features**:
- Ticket creation and management
- File attachment support (via MinIO)
- Comment threads
- Ticket assignment
- Priority and status tracking

**Models**:
- `Ticket` - Support tickets
- `TicketComment` - Ticket comments
- `TicketAttachment` - File attachments

**API Endpoints**:
- `POST /api/v1/support/tickets` - Create ticket
- `GET /api/v1/support/tickets` - List tickets
- `GET /api/v1/support/tickets/{id}` - Get ticket
- `PUT /api/v1/support/tickets/{id}` - Update ticket
- `POST /api/v1/support/tickets/{id}/comments` - Add comment
- `GET /api/v1/support/tickets/{id}/comments` - List comments
- `POST /api/v1/support/tickets/{id}/attachments` - Upload attachment
- `GET /api/v1/support/tickets/{id}/attachments` - List attachments

---

### 6. Themes Service (Port 8006)

**Purpose**: Dynamic theme management and branding per organization.

**Key Features**:
- Custom color schemes
- Logo and favicon management
- Custom CSS injection
- Public page content management
- Per-organization branding

**Models**:
- `Theme` - Organization themes
- `PublicPage` - Custom public pages

**API Endpoints**:
- `POST /api/v1/themes` - Create theme
- `GET /api/v1/themes` - Get organization theme
- `PUT /api/v1/themes` - Update theme
- `POST /api/v1/themes/pages` - Create public page
- `GET /api/v1/themes/pages` - List pages
- `GET /api/v1/themes/pages/{slug}` - Get page
- `PUT /api/v1/themes/pages/{slug}` - Update page
- `DELETE /api/v1/themes/pages/{slug}` - Delete page

---

### 7. Notifications Service (Port 8007)

**Purpose**: Multi-channel notifications with template management.

**Key Features**:
- Email notifications
- SMS support (optional)
- In-app notifications
- Push notifications
- Template management
- Delivery queue (via Redis)

**Models**:
- `Notification` - Notification records
- `NotificationTemplate` - Reusable templates

**API Endpoints**:
- `POST /api/v1/notifications` - Create notification
- `GET /api/v1/notifications` - List notifications
- `GET /api/v1/notifications/{id}` - Get notification
- `POST /api/v1/notifications/templates` - Create template
- `GET /api/v1/notifications/templates` - List templates
- `GET /api/v1/notifications/templates/{id}` - Get template
- `PUT /api/v1/notifications/templates/{id}` - Update template
- `DELETE /api/v1/notifications/templates/{id}` - Delete template

---

### 8. Workers Service (Port 8008)

**Purpose**: LangGraph workflow execution with job queues and monitoring.

**Key Features**:
- Job queue management
- Workflow execution
- Celery integration
- Job status tracking
- Workflow templates
- Retry logic

**Models**:
- `Job` - Worker jobs
- `WorkflowTemplate` - Reusable workflows

**API Endpoints**:
- `POST /api/v1/workers/jobs` - Create job
- `GET /api/v1/workers/jobs` - List jobs
- `GET /api/v1/workers/jobs/{id}` - Get job
- `POST /api/v1/workers/jobs/{id}/cancel` - Cancel job
- `POST /api/v1/workers/templates` - Create template
- `GET /api/v1/workers/templates` - List templates
- `GET /api/v1/workers/templates/{id}` - Get template
- `PUT /api/v1/workers/templates/{id}` - Update template
- `DELETE /api/v1/workers/templates/{id}` - Delete template

---

## Shared Components

### Authentication Middleware

Located in `services/shared/middleware/auth.py`, provides:
- JWT token validation
- User role checking
- RBAC enforcement
- Optional authentication

### Database Models

Base model in `services/shared/models/base.py`:
- `BaseModel` - Auto ID, timestamps
- `TimestampMixin` - created_at, updated_at
- `SoftDeleteMixin` - Soft delete support
- `TenantMixin` - Multi-tenant organization_id

### Security Utilities

Located in `services/shared/utils/security.py`:
- Password hashing with bcrypt
- JWT token creation/validation
- API key generation
- Password strength validation

### Configuration

Centralized settings in `services/shared/config/settings.py`:
- Database configuration
- Redis configuration
- JWT settings
- Email settings
- Stripe settings
- Feature flags

---

## Database Schema

The complete database schema is in `scripts/migration/init.sql` with tables for:
- Organizations and users
- Authentication tokens
- API keys and usage
- Subscriptions and billing
- Support tickets
- Themes and pages
- Notifications
- Worker jobs and workflows
- Audit logs

---

## Deployment

### Docker Compose

Start all services:
```bash
docker-compose up -d
```

### Individual Service

```bash
cd services/auth
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### Health Checks

Each service exposes:
- `GET /` - Service info
- `GET /health` - Health check
- `GET /docs` - Swagger UI
- `GET /redoc` - ReDoc

---

## Security

### Authentication Flow

1. User logs in via Auth Service
2. Receives JWT access token and refresh token
3. Access token used for API requests
4. Refresh token used to get new access tokens
5. All services validate JWT tokens

### API Key Authentication

1. Generate API key via Keys Service
2. Include in header: `Authorization: Bearer <api_key>`
3. Key validated and scoped permissions checked
4. Usage tracked automatically

### RBAC

Roles checked at endpoint level:
- `@Depends(get_current_user)` - Any authenticated user
- `@Depends(require_org_admin())` - Org admin or super admin
- `@Depends(require_super_admin())` - Super admin only

---

## Monitoring

### Prometheus

Metrics endpoint: `http://localhost:9090`

### Grafana

Dashboard: `http://localhost:3002`
- Default credentials: admin/admin

### Logs

Each service logs to stdout with configurable levels via `LOG_LEVEL` environment variable.

---

## Development

### Adding New Endpoints

1. Define Pydantic schemas in `schemas.py`
2. Create database models in `models.py`
3. Implement routes in `routes.py`
4. Include router in `main.py`

### Database Migrations

```bash
# Run initial migration
./scripts/setup/migrate.sh

# Connect to database
psql -h localhost -U vetrai -d vetrai_db
```

### Testing

Each service should have tests in `tests/` directory:
```bash
pytest services/auth/tests/
```

---

## Production Considerations

### Environment Variables

Set in `.env` file (see `.env.example`):
- Database credentials
- JWT secret keys
- Stripe API keys
- Email SMTP settings
- Redis password

### Scaling

- Run multiple instances of each service
- Use load balancer (nginx/traefik)
- Separate read replicas for PostgreSQL
- Redis cluster for high availability

### Security

- Use HTTPS in production
- Rotate JWT secrets regularly
- Enable audit logging
- Implement rate limiting
- Use secrets management (Vault/AWS Secrets Manager)

---

## Support

For issues and questions:
- GitHub Issues: https://github.com/bininfotech0/vetrai_v5/issues
- Documentation: docs.vetrai.io
- Email: support@vetrai.io
