# VetrAI Platform - API Documentation

Complete API reference for all VetrAI services.

## Table of Contents

- [Authentication](#authentication)
- [Services](#services)
  - [Authentication Service](#authentication-service)
  - [Tenancy Service](#tenancy-service)
  - [API Keys Service](#api-keys-service)
  - [Billing Service](#billing-service)
  - [Support Service](#support-service)
  - [Themes Service](#themes-service)
  - [Notifications Service](#notifications-service)
  - [Workers Service](#workers-service)
- [Error Handling](#error-handling)
- [Rate Limiting](#rate-limiting)

## Authentication

VetrAI uses JWT (JSON Web Tokens) for authentication. Include the access token in the Authorization header:

```
Authorization: Bearer <your_access_token>
```

### Token Types

1. **Access Token**: Short-lived (30 minutes), used for API requests
2. **Refresh Token**: Long-lived (7 days), used to obtain new access tokens

## Services

### Authentication Service

**Base URL**: `http://localhost:8001/api/v1`

#### Register User

```http
POST /register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "SecurePass123!",
  "first_name": "John",
  "last_name": "Doe",
  "organization_id": 1,
  "role": "user"
}
```

**Response** (201 Created):
```json
{
  "id": 1,
  "email": "user@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "role": "user",
  "organization_id": 1,
  "is_active": true,
  "is_verified": false,
  "created_at": "2024-01-01T00:00:00Z",
  "last_login": null
}
```

#### Login

```http
POST /login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "SecurePass123!"
}
```

**Response** (200 OK):
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "role": "user",
    "organization_id": 1,
    "is_active": true,
    "is_verified": false,
    "created_at": "2024-01-01T00:00:00Z",
    "last_login": "2024-01-01T12:00:00Z"
  }
}
```

#### Refresh Token

```http
POST /refresh
Content-Type: application/json

{
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Response** (200 OK):
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer"
}
```

#### Get Current User

```http
GET /me
Authorization: Bearer <access_token>
```

**Response** (200 OK):
```json
{
  "id": 1,
  "email": "user@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "role": "user",
  "organization_id": 1,
  "is_active": true,
  "is_verified": false,
  "created_at": "2024-01-01T00:00:00Z",
  "last_login": "2024-01-01T12:00:00Z"
}
```

#### Update Current User

```http
PUT /me
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "first_name": "Jane",
  "last_name": "Smith"
}
```

**Response** (200 OK):
```json
{
  "id": 1,
  "email": "user@example.com",
  "first_name": "Jane",
  "last_name": "Smith",
  ...
}
```

#### Change Password

```http
POST /change-password
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "old_password": "OldPass123!",
  "new_password": "NewSecurePass456!"
}
```

**Response** (200 OK):
```json
{
  "message": "Password changed successfully"
}
```

#### List Users (Admin)

```http
GET /users?skip=0&limit=100
Authorization: Bearer <access_token>
```

**Response** (200 OK):
```json
[
  {
    "id": 1,
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    ...
  },
  ...
]
```

### Tenancy Service

**Base URL**: `http://localhost:8002/api/v1`

#### Create Organization (Super Admin)

```http
POST /organizations
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "name": "ACME Corporation",
  "slug": "acme",
  "domain": "acme.com",
  "plan": "enterprise",
  "max_users": 100,
  "max_api_keys": 200,
  "settings": {
    "feature_x": true,
    "feature_y": false
  }
}
```

**Response** (201 Created):
```json
{
  "id": 1,
  "name": "ACME Corporation",
  "slug": "acme",
  "domain": "acme.com",
  "plan": "enterprise",
  "is_active": true,
  "max_users": 100,
  "max_api_keys": 200,
  "settings": {
    "feature_x": true,
    "feature_y": false
  },
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

#### List Organizations

```http
GET /organizations?skip=0&limit=100
Authorization: Bearer <access_token>
```

**Response** (200 OK):
```json
[
  {
    "id": 1,
    "name": "ACME Corporation",
    "slug": "acme",
    ...
  },
  ...
]
```

#### Get Organization

```http
GET /organizations/{org_id}
Authorization: Bearer <access_token>
```

**Response** (200 OK):
```json
{
  "id": 1,
  "name": "ACME Corporation",
  "slug": "acme",
  ...
}
```

#### Update Organization

```http
PUT /organizations/{org_id}
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "name": "ACME Corp",
  "plan": "pro",
  "settings": {
    "feature_z": true
  }
}
```

**Response** (200 OK):
```json
{
  "id": 1,
  "name": "ACME Corp",
  "plan": "pro",
  ...
}
```

#### Delete Organization (Super Admin)

```http
DELETE /organizations/{org_id}
Authorization: Bearer <access_token>
```

**Response** (200 OK):
```json
{
  "message": "Organization deleted successfully"
}
```

### API Keys Service

**Base URL**: `http://localhost:8003/api/v1`

#### Create API Key

```http
POST /keys
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "name": "Production API Key",
  "scopes": ["read", "write", "admin"],
  "expires_at": "2025-12-31T23:59:59Z"
}
```

**Response** (201 Created):
```json
{
  "id": 1,
  "name": "Production API Key",
  "key": "vetrai_abc123def456...",
  "key_prefix": "vetrai_abc1",
  "scopes": ["read", "write", "admin"],
  "is_active": true,
  "expires_at": "2025-12-31T23:59:59Z",
  "created_at": "2024-01-01T00:00:00Z"
}
```

**⚠️ Note**: The full API key is only shown once. Store it securely!

#### List API Keys

```http
GET /keys?skip=0&limit=100
Authorization: Bearer <access_token>
```

**Response** (200 OK):
```json
[
  {
    "id": 1,
    "name": "Production API Key",
    "key_prefix": "vetrai_abc1",
    "scopes": ["read", "write", "admin"],
    "is_active": true,
    "expires_at": "2025-12-31T23:59:59Z",
    "last_used_at": "2024-01-15T10:30:00Z",
    "usage_count": 1234,
    "created_at": "2024-01-01T00:00:00Z"
  },
  ...
]
```

#### Validate API Key

```http
POST /keys/validate
Content-Type: application/json

{
  "api_key": "vetrai_abc123def456..."
}
```

**Response** (200 OK):
```json
{
  "valid": true,
  "organization_id": 1,
  "user_id": 1,
  "scopes": ["read", "write", "admin"]
}
```

#### Revoke API Key

```http
DELETE /keys/{key_id}
Authorization: Bearer <access_token>
```

**Response** (200 OK):
```json
{
  "message": "API key revoked successfully"
}
```

## Error Handling

All API endpoints follow a consistent error response format:

```json
{
  "detail": "Error message describing what went wrong"
}
```

### HTTP Status Codes

- **200 OK**: Request succeeded
- **201 Created**: Resource created successfully
- **400 Bad Request**: Invalid request data
- **401 Unauthorized**: Missing or invalid authentication
- **403 Forbidden**: Insufficient permissions
- **404 Not Found**: Resource not found
- **422 Unprocessable Entity**: Validation error
- **429 Too Many Requests**: Rate limit exceeded
- **500 Internal Server Error**: Server error

### Error Examples

**400 Bad Request**:
```json
{
  "detail": "Email already registered"
}
```

**401 Unauthorized**:
```json
{
  "detail": "Could not validate credentials"
}
```

**403 Forbidden**:
```json
{
  "detail": "Insufficient permissions"
}
```

**422 Validation Error**:
```json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "value is not a valid email address",
      "type": "value_error.email"
    }
  ]
}
```

## Rate Limiting

VetrAI implements rate limiting to protect services:

- **Per User**: 60 requests/minute, 1000 requests/hour
- **Per API Key**: Configurable per key
- **Per IP**: 100 requests/minute (anonymous)

### Rate Limit Headers

Responses include rate limit information:

```
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 45
X-RateLimit-Reset: 1609459200
```

### Rate Limit Exceeded

```http
HTTP/1.1 429 Too Many Requests
Content-Type: application/json

{
  "detail": "Rate limit exceeded. Retry after 30 seconds."
}
```

## Pagination

List endpoints support pagination:

```http
GET /api/v1/users?skip=0&limit=100
```

**Parameters**:
- `skip`: Number of records to skip (default: 0)
- `limit`: Maximum records to return (default: 100, max: 1000)

## Filtering & Sorting

Many endpoints support filtering and sorting:

```http
GET /api/v1/users?role=admin&is_active=true&sort_by=created_at&order=desc
```

## Webhooks

VetrAI can send webhooks for important events:

- User registration
- Subscription changes
- Payment events
- Ticket updates

Configure webhooks in organization settings.

## SDKs

Official SDKs are available for:

- **Python**: `pip install vetrai-sdk`
- **JavaScript/TypeScript**: `npm install @vetrai/sdk`
- **Go**: `go get github.com/vetrai/go-sdk`

## Support

For API support:
- **Documentation**: [https://docs.vetrai.io](https://docs.vetrai.io)
- **API Status**: [https://status.vetrai.io](https://status.vetrai.io)
- **Email**: api-support@vetrai.io

---

For more detailed examples, see the [API Examples](examples/) directory.
