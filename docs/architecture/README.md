# VetrAI Platform Architecture

## Overview

VetrAI is built as a microservices-based platform with a focus on scalability, maintainability, and multi-tenancy. This document provides a comprehensive overview of the system architecture.

## Table of Contents

- [System Architecture](#system-architecture)
- [Service Architecture](#service-architecture)
- [Data Architecture](#data-architecture)
- [Security Architecture](#security-architecture)
- [Deployment Architecture](#deployment-architecture)
- [Technology Stack](#technology-stack)

## System Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         Client Layer                             │
│  ┌──────────┐    ┌───────────────┐    ┌──────────────┐        │
│  │  Studio  │    │ Admin Dashboard│    │Public Website│        │
│  │ (React)  │    │    (React)     │    │   (React)    │        │
│  └──────────┘    └───────────────┘    └──────────────┘        │
└────────────────────────┬────────────────────────────────────────┘
                         │ HTTPS
┌────────────────────────┼────────────────────────────────────────┐
│                        │  API Gateway / Load Balancer            │
│                   ┌────┴────┐                                    │
│                   │  Nginx  │                                    │
│                   └────┬────┘                                    │
└────────────────────────┼────────────────────────────────────────┘
                         │
┌────────────────────────┼────────────────────────────────────────┐
│                 Service Layer (FastAPI)                          │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐       │
│  │   Auth   │  │ Tenancy  │  │   Keys   │  │ Billing  │       │
│  │ Service  │  │ Service  │  │ Service  │  │ Service  │       │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘       │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐       │
│  │ Support  │  │  Themes  │  │ Notific. │  │ Workers  │       │
│  │ Service  │  │ Service  │  │ Service  │  │ Service  │       │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘       │
└────────────────────────┬────────────────────────────────────────┘
                         │
┌────────────────────────┼────────────────────────────────────────┐
│                 Data Layer                                       │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐       │
│  │PostgreSQL│  │  Redis   │  │  MinIO   │  │  Stripe  │       │
│  │(Primary) │  │ (Cache)  │  │(Storage) │  │(Payment) │       │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘       │
└─────────────────────────────────────────────────────────────────┘
```

### Design Principles

1. **Microservices Architecture**: Each service is independent and focused on a specific domain
2. **Multi-Tenancy**: Data isolation at the organization level
3. **Scalability**: Horizontal scaling of services
4. **Security First**: Authentication, authorization, and encryption at all layers
5. **Event-Driven**: Asynchronous communication where appropriate
6. **API-First**: Well-documented REST APIs

## Service Architecture

### 1. Authentication Service

**Responsibility**: User authentication, JWT token management, RBAC

**Endpoints**:
- `POST /api/v1/register` - User registration
- `POST /api/v1/login` - User login
- `POST /api/v1/refresh` - Token refresh
- `POST /api/v1/logout` - User logout
- `GET /api/v1/me` - Current user info
- `POST /api/v1/change-password` - Password change

**Database Tables**:
- `users`
- `refresh_tokens`
- `audit_logs`

**Dependencies**:
- PostgreSQL (user data)
- Redis (token blacklist)

### 2. Tenancy Service

**Responsibility**: Organization management, multi-tenant support

**Endpoints**:
- `POST /api/v1/organizations` - Create organization
- `GET /api/v1/organizations` - List organizations
- `GET /api/v1/organizations/{id}` - Get organization
- `PUT /api/v1/organizations/{id}` - Update organization
- `DELETE /api/v1/organizations/{id}` - Delete organization

**Database Tables**:
- `organizations`

**Features**:
- Tenant isolation middleware
- Plan management
- Usage limits enforcement

### 3. API Key Management Service

**Responsibility**: Secure API key generation, management, and validation

**Endpoints**:
- `POST /api/v1/keys` - Create API key
- `GET /api/v1/keys` - List API keys
- `GET /api/v1/keys/{id}` - Get API key details
- `DELETE /api/v1/keys/{id}` - Revoke API key
- `POST /api/v1/keys/validate` - Validate API key

**Database Tables**:
- `api_keys`
- `usage_tracking`

**Features**:
- Scoped permissions
- Rate limiting
- Usage analytics

### 4. Billing Service

**Responsibility**: Stripe integration, subscription management

**Endpoints**:
- `POST /api/v1/subscriptions` - Create subscription
- `GET /api/v1/subscriptions` - List subscriptions
- `PUT /api/v1/subscriptions/{id}` - Update subscription
- `DELETE /api/v1/subscriptions/{id}` - Cancel subscription
- `GET /api/v1/invoices` - List invoices
- `POST /api/v1/webhooks/stripe` - Stripe webhooks

**Database Tables**:
- `subscriptions`
- `invoices`

**External Integrations**:
- Stripe API
- Razorpay API (optional)

### 5. Support Service

**Responsibility**: Ticketing system, SLA management

**Endpoints**:
- `POST /api/v1/tickets` - Create ticket
- `GET /api/v1/tickets` - List tickets
- `GET /api/v1/tickets/{id}` - Get ticket
- `PUT /api/v1/tickets/{id}` - Update ticket
- `POST /api/v1/tickets/{id}/comments` - Add comment
- `POST /api/v1/tickets/{id}/attachments` - Upload attachment

**Database Tables**:
- `tickets`
- `ticket_comments`

**Features**:
- File attachments (MinIO)
- SLA tracking
- Assignment workflows
- Email notifications

### 6. Themes Service

**Responsibility**: Dynamic theming, branding management

**Endpoints**:
- `POST /api/v1/themes` - Create theme
- `GET /api/v1/themes` - List themes
- `GET /api/v1/themes/{id}` - Get theme
- `PUT /api/v1/themes/{id}` - Update theme
- `POST /api/v1/themes/{id}/logo` - Upload logo

**Database Tables**:
- `themes`

**Features**:
- Logo/favicon management
- Color customization
- Custom CSS/JS
- Per-organization theming

### 7. Notifications Service

**Responsibility**: Multi-channel notifications

**Endpoints**:
- `POST /api/v1/notifications/send` - Send notification
- `GET /api/v1/notifications` - List notifications
- `PUT /api/v1/notifications/{id}/read` - Mark as read
- `GET /api/v1/notifications/preferences` - Get preferences
- `PUT /api/v1/notifications/preferences` - Update preferences

**Database Tables**:
- `notifications`
- `notification_templates`

**Channels**:
- Email (SMTP)
- SMS (Twilio)
- In-app notifications

### 8. Workers Service

**Responsibility**: LangGraph integration, async job execution

**Endpoints**:
- `POST /api/v1/jobs` - Create job
- `GET /api/v1/jobs` - List jobs
- `GET /api/v1/jobs/{id}` - Get job status
- `DELETE /api/v1/jobs/{id}` - Cancel job

**Database Tables**:
- `worker_jobs`

**Features**:
- Celery task queue
- Retry mechanisms
- Job monitoring
- LangGraph integration

## Data Architecture

### Database Schema

#### Multi-Tenancy Pattern

```sql
-- Organization table (tenant root)
CREATE TABLE organizations (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    slug VARCHAR(100) UNIQUE,
    plan VARCHAR(50),
    ...
);

-- All tenant data references organization_id
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    organization_id INTEGER REFERENCES organizations(id),
    email VARCHAR(255),
    ...
);
```

#### Indexing Strategy

- Primary keys: SERIAL with indexes
- Foreign keys: Always indexed
- Query columns: email, organization_id, status fields
- Timestamp columns: created_at for time-based queries

### Data Flow

1. **Write Path**:
   ```
   Client → API Gateway → Service → PostgreSQL
                                  ↓
                              Redis (cache invalidation)
   ```

2. **Read Path**:
   ```
   Client → API Gateway → Service → Redis (cache hit)
                                  ↓
                              PostgreSQL (cache miss)
   ```

## Security Architecture

### Authentication Flow

```
1. User submits credentials
2. Auth service validates against database
3. Generate JWT access token (30 min expiry)
4. Generate refresh token (7 day expiry)
5. Store refresh token in database
6. Return both tokens to client
7. Client includes access token in subsequent requests
8. Services validate JWT signature and expiry
9. Extract user context from token claims
```

### Authorization

**Role-Based Access Control (RBAC)**:

```
super_admin → Full system access
org_admin → Organization-level access
user → Basic user access
support_agent → Support ticket access
billing_admin → Billing and subscription access
```

### Security Layers

1. **Transport Layer**: TLS/SSL for all communications
2. **Application Layer**: JWT tokens, API keys
3. **Data Layer**: Encrypted at rest, tenant isolation
4. **Network Layer**: Firewall rules, VPC isolation

### Data Protection

- Password hashing: bcrypt with salt
- Token encryption: HS256 JWT
- API key hashing: SHA-256
- Sensitive data: AES-256 encryption
- PII compliance: GDPR-ready with data export/deletion

## Deployment Architecture

### Docker Compose (Development)

```yaml
services:
  - postgres (database)
  - redis (cache/queue)
  - minio (storage)
  - auth-service
  - tenancy-service
  - ... (other services)
  - prometheus (monitoring)
  - grafana (visualization)
```

### Kubernetes (Production)

```
Namespace: vetrai-production
├── Deployments
│   ├── auth-service (3 replicas)
│   ├── tenancy-service (2 replicas)
│   ├── ... (other services)
│   ├── nginx-ingress (2 replicas)
├── StatefulSets
│   ├── postgresql (primary-replica)
│   ├── redis (cluster mode)
├── Services
│   ├── LoadBalancer (external)
│   ├── ClusterIP (internal)
├── ConfigMaps
│   ├── service-configs
├── Secrets
│   ├── database-credentials
│   ├── api-keys
│   ├── stripe-keys
└── PersistentVolumeClaims
    ├── postgres-data
    ├── redis-data
    ├── minio-data
```

### Scaling Strategy

**Horizontal Scaling**:
- Stateless services: Scale based on CPU/memory
- Worker services: Scale based on queue depth
- Database: Read replicas for read-heavy workloads

**Vertical Scaling**:
- Database: Increase resources for complex queries
- Cache: Increase memory for larger working set

## Technology Stack

### Backend
- **Framework**: FastAPI 0.104+
- **Language**: Python 3.11+
- **ASGI Server**: Uvicorn
- **ORM**: SQLAlchemy 2.0+
- **Migrations**: Alembic

### Database
- **Primary**: PostgreSQL 15+ with pgvector
- **Cache**: Redis 7+
- **Storage**: MinIO (S3-compatible)

### Frontend
- **Framework**: React 18+
- **Language**: TypeScript 5+
- **Build Tool**: Vite
- **UI Library**: Tailwind CSS + shadcn/ui

### Infrastructure
- **Containerization**: Docker
- **Orchestration**: Kubernetes + Helm
- **IaC**: Terraform
- **CI/CD**: GitHub Actions
- **Monitoring**: Prometheus + Grafana

### External Services
- **Payments**: Stripe, Razorpay
- **Email**: SMTP (SendGrid, Mailgun)
- **SMS**: Twilio

## Performance Considerations

### Caching Strategy

1. **Application Cache**: Redis for frequently accessed data
2. **Database Cache**: PostgreSQL query cache
3. **CDN**: Static assets and public pages

### Database Optimization

1. **Connection Pooling**: SQLAlchemy pool (20 connections)
2. **Query Optimization**: Proper indexes, query analysis
3. **Read Replicas**: For reporting and analytics

### API Optimization

1. **Rate Limiting**: Per user, per API key
2. **Pagination**: Cursor-based for large datasets
3. **Compression**: Gzip for API responses

## Monitoring & Observability

### Metrics

- Service health endpoints
- Request/response times
- Error rates
- Resource usage (CPU, memory, disk)

### Logging

- Structured logging (JSON format)
- Log levels: DEBUG, INFO, WARNING, ERROR
- Centralized logging with ELK stack

### Tracing

- Distributed tracing with OpenTelemetry
- Request correlation IDs

## Disaster Recovery

### Backup Strategy

- **Database**: Daily backups, 30-day retention
- **Object Storage**: Cross-region replication
- **Configuration**: Version controlled in Git

### Recovery Procedures

1. Database restore from backup
2. Service redeployment from container images
3. Configuration restore from Git
4. DNS failover to backup region

---

For more detailed information on specific components, see:
- [API Documentation](../api/README.md)
- [Deployment Guide](../deployment/README.md)
- [Development Guide](../guides/development.md)
