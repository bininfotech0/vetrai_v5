# VetrAI Auth Service - Opaque Access Tokens

This authentication service implements opaque (server-side) access tokens with database storage instead of JWT tokens.

## Overview

- **Access Tokens**: Opaque tokens (random 32-byte URL-safe strings) stored hashed in the database
- **Refresh Tokens**: Opaque tokens stored hashed in the database
- **Token Storage**: SHA256 hashes stored in AccessToken and RefreshToken tables
- **Immediate Revocation**: Tokens can be revoked immediately via database deletion
- **Token Rotation**: Refresh endpoint revokes all existing tokens and issues new ones

## Key Changes from JWT-based Auth

### Before (JWT)
- Access tokens were self-contained JWT tokens
- No database lookup required for validation
- Could not be revoked immediately (had to wait for expiry)
- Server-side state not required

### After (Opaque Tokens)
- Access tokens are random opaque strings
- Database lookup required for every validation
- Can be revoked immediately by deleting from database
- Full server-side control over token lifecycle

## Database Schema

### AccessToken Table
```sql
CREATE TABLE accesstoken (
    id VARCHAR PRIMARY KEY,
    user_id VARCHAR FOREIGN KEY -> user(id),
    token_hash VARCHAR,  -- SHA256 hash of the token
    created_at DATETIME,
    expires_at DATETIME
)
```

### RefreshToken Table
```sql
CREATE TABLE refreshtoken (
    id VARCHAR PRIMARY KEY,
    user_id VARCHAR FOREIGN KEY -> user(id),
    token_hash VARCHAR,  -- SHA256 hash of the token
    created_at DATETIME,
    expires_at DATETIME
)
```

## API Endpoints

### POST /register
Register a new user.

**Request:**
```json
{
  "email": "user@example.com",
  "password": "securepassword",
  "name": "User Name"
}
```

**Response:**
```json
{
  "id": "uuid",
  "email": "user@example.com",
  "name": "User Name"
}
```

### POST /login
Login and receive access + refresh tokens.

**Request:**
```json
{
  "email": "user@example.com",
  "password": "securepassword"
}
```

**Response:**
```json
{
  "access_token": "iAkqzyX6LJg6kpkcT1ZkL4xN...",
  "token_type": "bearer",
  "refresh_token": "31d26aab224ffef8e88c3a9b..."
}
```

### POST /refresh
Refresh tokens (rotates both access and refresh tokens).

**Request:**
```json
{
  "user_id": "uuid",
  "refresh_token": "31d26aab224ffef8e88c3a9b..."
}
```

**Response:**
```json
{
  "access_token": "p0PapTIFz6jSyr4rT54x...",
  "token_type": "bearer",
  "refresh_token": "8f1d9c2b113ade7f9a2c..."
}
```

### GET /users/me
Get current user information (requires Bearer token).

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response:**
```json
{
  "id": "uuid",
  "email": "user@example.com",
  "name": "User Name"
}
```

## Running the Service

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Start the Service
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Environment Variables
- `DATABASE_URL`: Database connection string (default: `sqlite:///./vetrai_auth.db`)
- `ACCESS_TOKEN_EXPIRE_SECONDS`: Access token TTL (default: 900 = 15 minutes)
- `REFRESH_TOKEN_EXPIRE_SECONDS`: Refresh token TTL (default: 2592000 = 30 days)

## Security Benefits

1. **Immediate Revocation**: Tokens can be revoked instantly by deleting from database
2. **Server-Side Control**: Full control over token lifecycle and validation
3. **Token Rotation**: Refresh endpoint implements full token rotation for enhanced security
4. **Hashed Storage**: Only SHA256 hashes stored in database, not raw tokens
5. **Automatic Expiry**: Expired tokens are automatically removed during verification

## Trade-offs

### Pros
- Immediate token revocation capability
- Full audit trail of active tokens
- Per-user token management
- No JWT signature verification overhead

### Cons
- Database lookup required for every request
- Higher database load
- Requires database availability for auth
- No distributed/stateless validation
