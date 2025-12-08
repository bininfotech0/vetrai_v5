# VetrAI Platform - Service API Documentation

This document provides a comprehensive overview of all service endpoints in the VetrAI platform.

## Service Ports

| Service | Port | Description |
|---------|------|-------------|
| Auth | 8001 | Authentication and user management |
| Tenancy | 8002 | Organization and tenant management |
| Keys | 8003 | API key management |
| Billing | 8004 | Billing and subscriptions |
| Support | 8005 | Support ticketing |
| Themes | 8006 | Theme customization |
| Notifications | 8007 | Notification management |
| Workers | 8008 | Background job execution |

## API Keys Service (Port 8003)

### Create API Key
**POST** `/api/v1/keys`

Creates a new API key with specified scopes and expiration.

**Request Body:**
```json
{
  "name": "My API Key",
  "scopes": ["read", "write"],
  "expires_days": 365
}
```

**Response:** (Status 201)
```json
{
  "id": 1,
  "organization_id": 1,
  "user_id": 1,
  "name": "My API Key",
  "key": "vetrai_abc123...",  // Only shown once!
  "key_prefix": "vetrai_a...123",
  "scopes": ["read", "write"],
  "is_active": true,
  "expires_at": "2025-12-08T00:00:00Z",
  "usage_count": 0,
  "created_at": "2024-12-08T00:00:00Z"
}
```

### List API Keys
**GET** `/api/v1/keys`

Lists all API keys for the authenticated user (keys are masked).

**Query Parameters:**
- `skip`: int (default: 0)
- `limit`: int (default: 100)

**Response:** (Status 200)
```json
[
  {
    "id": 1,
    "key_prefix": "vetrai_a...123",
    "name": "My API Key",
    "scopes": ["read", "write"],
    "usage_count": 42,
    "last_used_at": "2024-12-08T12:00:00Z"
  }
]
```

### Get API Key
**GET** `/api/v1/keys/{key_id}`

Gets details of a specific API key (masked).

### Update API Key
**PUT** `/api/v1/keys/{key_id}`

Updates API key scopes, expiry, or active status.

**Request Body:**
```json
{
  "name": "Updated Name",
  "scopes": ["read"],
  "is_active": true
}
```

### Delete API Key
**DELETE** `/api/v1/keys/{key_id}`

Revokes/deactivates an API key.

### Get Usage Statistics
**GET** `/api/v1/keys/{key_id}/usage`

Gets usage statistics for an API key.

**Response:**
```json
{
  "total_requests": 1000,
  "success_requests": 950,
  "failed_requests": 50,
  "avg_response_time_ms": 123.45,
  "requests_by_endpoint": {
    "/api/v1/users": 500,
    "/api/v1/workflows": 500
  }
}
```

---

## Billing Service (Port 8004)

### Create Customer
**POST** `/api/v1/customers`

Creates a Stripe customer for the organization.

### Create Subscription
**POST** `/api/v1/subscriptions`

Creates a new subscription for the organization.

**Request Body:**
```json
{
  "plan": "pro",
  "payment_method_id": "pm_123"
}
```

### List Subscriptions
**GET** `/api/v1/subscriptions`

Lists all subscriptions for the organization.

### Create Checkout Session
**POST** `/api/v1/checkout`

Creates a Stripe checkout session.

**Request Body:**
```json
{
  "plan": "pro",
  "success_url": "https://app.example.com/success",
  "cancel_url": "https://app.example.com/cancel"
}
```

**Response:**
```json
{
  "session_id": "cs_test_123",
  "url": "https://checkout.stripe.com/pay/cs_test_123"
}
```

### Stripe Webhook
**POST** `/api/v1/webhooks/stripe`

Handles Stripe webhook events (internal use).

### List Invoices
**GET** `/api/v1/invoices`

Lists invoices for the organization.

---

## Support Service (Port 8005)

### Create Ticket
**POST** `/api/v1/tickets`

Creates a new support ticket.

**Request Body:**
```json
{
  "title": "Issue with workflow",
  "description": "Detailed description...",
  "priority": "high",
  "category": "technical"
}
```

**Response:** (Status 201)
```json
{
  "id": 1,
  "organization_id": 1,
  "user_id": 1,
  "title": "Issue with workflow",
  "description": "Detailed description...",
  "status": "open",
  "priority": "high",
  "category": "technical",
  "created_at": "2024-12-08T00:00:00Z"
}
```

### List Tickets
**GET** `/api/v1/tickets`

Lists tickets for the organization.

**Query Parameters:**
- `status`: string (open, in_progress, resolved, closed)
- `skip`: int
- `limit`: int

### Get Ticket
**GET** `/api/v1/tickets/{ticket_id}`

Gets details of a specific ticket.

### Update Ticket
**PUT** `/api/v1/tickets/{ticket_id}`

Updates ticket status, priority, or assignment.

**Request Body:**
```json
{
  "status": "in_progress",
  "priority": "high",
  "assigned_to": 5
}
```

### Add Comment
**POST** `/api/v1/tickets/{ticket_id}/comments`

Adds a comment to a ticket.

**Request Body:**
```json
{
  "comment": "Working on this issue...",
  "is_internal": false
}
```

### Upload Attachment
**POST** `/api/v1/tickets/{ticket_id}/attachments`

Uploads a file attachment to a ticket.

**Request:** multipart/form-data with `file` field

---

## Themes Service (Port 8006)

### Get Theme
**GET** `/api/v1/themes/{org_id}`

Gets the theme for an organization (public endpoint).

**Response:**
```json
{
  "id": 1,
  "organization_id": 1,
  "name": "Custom Theme",
  "logo_url": "https://...",
  "primary_color": "#3b82f6",
  "secondary_color": "#64748b",
  "accent_color": "#f59e0b",
  "custom_css": "...",
  "is_active": true
}
```

### Update Theme
**PUT** `/api/v1/themes/{org_id}`

Updates theme settings (admin only).

**Request Body:**
```json
{
  "name": "Updated Theme",
  "primary_color": "#ff0000",
  "secondary_color": "#00ff00",
  "custom_css": ".custom { color: red; }"
}
```

### Upload Logo
**POST** `/api/v1/themes/{org_id}/logo`

Uploads organization logo (admin only).

**Request:** multipart/form-data with `file` field

### Generate CSS
**GET** `/api/v1/themes/{org_id}/css`

Generates CSS from theme settings.

**Response:** CSS text

---

## Notifications Service (Port 8007)

### Send Notification
**POST** `/api/v1/notifications`

Sends a notification to a user.

**Request Body:**
```json
{
  "user_id": 1,
  "title": "New Message",
  "message": "You have a new message...",
  "type": "info",
  "channel": "email",
  "metadata": {}
}
```

### List Notifications
**GET** `/api/v1/notifications`

Lists notifications for the authenticated user.

**Query Parameters:**
- `is_read`: boolean
- `skip`: int
- `limit`: int

**Response:**
```json
[
  {
    "id": 1,
    "title": "New Message",
    "message": "You have a new message...",
    "type": "info",
    "channel": "email",
    "is_read": false,
    "created_at": "2024-12-08T00:00:00Z"
  }
]
```

### Mark as Read
**PUT** `/api/v1/notifications/{notification_id}/read`

Marks a notification as read.

### Get Preferences
**GET** `/api/v1/preferences`

Gets notification preferences for the user.

**Response:**
```json
{
  "email_enabled": true,
  "in_app_enabled": true,
  "sms_enabled": false
}
```

### Update Preferences
**PUT** `/api/v1/preferences`

Updates notification preferences.

---

## Workers Service (Port 8008)

### Execute Workflow
**POST** `/api/v1/workflows/execute`

Executes a workflow asynchronously.

**Request Body:**
```json
{
  "workflow_type": "data_processing",
  "input_data": {
    "source": "csv",
    "file_path": "/data/input.csv"
  },
  "priority": 5
}
```

**Response:** (Status 201)
```json
{
  "job_id": 1,
  "status": "pending",
  "message": "Workflow execution started"
}
```

### Get Workflow Status
**GET** `/api/v1/workflows/{job_id}`

Gets the status of a workflow execution.

**Response:**
```json
{
  "id": 1,
  "organization_id": 1,
  "user_id": 1,
  "job_type": "data_processing",
  "status": "completed",
  "input_data": {...},
  "output_data": {...},
  "started_at": "2024-12-08T00:00:00Z",
  "completed_at": "2024-12-08T00:01:30Z"
}
```

### Cancel Workflow
**DELETE** `/api/v1/workflows/{job_id}`

Cancels a running workflow.

### Get Metrics
**GET** `/api/v1/metrics`

Gets workflow execution metrics for the organization.

**Response:**
```json
{
  "total_jobs": 1000,
  "pending_jobs": 5,
  "running_jobs": 3,
  "completed_jobs": 990,
  "failed_jobs": 2,
  "avg_execution_time_seconds": 45.5
}
```

---

## Authentication

All endpoints (except public ones) require authentication:

### JWT Token Authentication
```
Authorization: Bearer <jwt_token>
```

### API Key Authentication
```
X-API-Key: vetrai_<key>
```

## Error Responses

Standard error format:

```json
{
  "detail": "Error message",
  "status_code": 400
}
```

Common status codes:
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
- 422: Validation Error
- 429: Too Many Requests (rate limited)
- 500: Internal Server Error

## Rate Limiting

Rate limits vary by endpoint and organization plan:

Headers:
```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1234567890
```

## Pagination

List endpoints support pagination:

Query parameters:
- `skip`: Number of items to skip (default: 0)
- `limit`: Maximum items to return (default: 100, max: 100)

Response headers:
```
X-Total-Count: 1234
X-Page: 1
X-Per-Page: 100
```

## Filtering & Sorting

Some endpoints support filtering and sorting:

```
GET /api/v1/tickets?status=open&priority=high&sort=created_at&order=desc
```

## Webhooks

Services can trigger webhooks for important events. Configure webhooks in the organization settings.

Example webhook payload:
```json
{
  "event": "ticket.created",
  "data": {
    "id": 1,
    "title": "New ticket"
  },
  "timestamp": "2024-12-08T00:00:00Z"
}
```

## SDK Support

Official SDKs are available for:
- Python
- JavaScript/TypeScript
- Go
- Java

See [SDK Documentation](../sdk/) for usage examples.
