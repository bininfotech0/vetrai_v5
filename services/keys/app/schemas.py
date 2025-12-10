"""
Pydantic schemas for API Keys Service
"""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field


class APIKeyCreate(BaseModel):
    """Schema for creating an API key"""
    name: str = Field(..., min_length=1, max_length=100)
    scopes: List[str] = Field(default_factory=list)
    rate_limit: Optional[int] = Field(None, gt=0)
    expires_at: Optional[datetime] = None


class APIKeyUpdate(BaseModel):
    """Schema for updating an API key"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    scopes: Optional[List[str]] = None
    rate_limit: Optional[int] = Field(None, gt=0)
    is_active: Optional[bool] = None


class APIKeyResponse(BaseModel):
    """Schema for API key response"""
    id: int
    name: str
    key_prefix: str
    user_id: int
    organization_id: int
    scopes: List[str]
    rate_limit: Optional[int]
    is_active: bool
    expires_at: Optional[datetime]
    last_used_at: Optional[datetime]
    created_at: datetime
    
    class Config:
        from_attributes = True


class APIKeyCreateResponse(APIKeyResponse):
    """Schema for API key creation response (includes full key)"""
    key: str


class APIKeyUsageResponse(BaseModel):
    """Schema for API key usage response"""
    id: int
    api_key_id: int
    endpoint: str
    method: str
    status_code: int
    response_time_ms: Optional[int]
    created_at: datetime
    
    class Config:
        from_attributes = True


class MessageResponse(BaseModel):
    """Generic message response"""
    message: str
