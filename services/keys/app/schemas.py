"""
Pydantic schemas for API Keys Service
"""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field


class APIKeyCreate(BaseModel):
    """Schema for creating a new API key"""
    name: str = Field(..., min_length=1, max_length=255)
    scopes: List[str] = Field(default=["read"])
    expires_days: Optional[int] = Field(None, ge=1, le=365)


class APIKeyUpdate(BaseModel):
    """Schema for updating an API key"""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    scopes: Optional[List[str]] = None
    is_active: Optional[bool] = None
    expires_at: Optional[datetime] = None


class APIKeyResponse(BaseModel):
    """Schema for API key response (masked)"""
    id: int
    organization_id: int
    user_id: int
    name: str
    key_prefix: str
    scopes: List[str]
    is_active: bool
    expires_at: Optional[datetime]
    last_used_at: Optional[datetime]
    usage_count: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class APIKeyCreateResponse(APIKeyResponse):
    """Schema for API key creation response (includes full key once)"""
    key: str  # Full key returned only once


class APIKeyUsageStats(BaseModel):
    """Schema for API key usage statistics"""
    total_requests: int
    success_requests: int
    failed_requests: int
    avg_response_time_ms: float
    requests_by_endpoint: dict


class MessageResponse(BaseModel):
    """Generic message response"""
    message: str
