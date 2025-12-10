"""
Pydantic schemas for Tenancy Service
"""
from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field


class OrganizationBase(BaseModel):
    """Base organization schema"""
    name: str = Field(..., min_length=1, max_length=255)
    slug: str = Field(..., min_length=1, max_length=100)
    domain: Optional[str] = Field(None, max_length=255)


class OrganizationCreate(OrganizationBase):
    """Schema for creating an organization"""
    plan: str = "free"
    max_users: int = 5
    max_api_keys: int = 10
    settings: Dict[str, Any] = {}


class OrganizationUpdate(BaseModel):
    """Schema for updating an organization"""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    domain: Optional[str] = Field(None, max_length=255)
    plan: Optional[str] = None
    is_active: Optional[bool] = None
    max_users: Optional[int] = None
    max_api_keys: Optional[int] = None
    settings: Optional[Dict[str, Any]] = None


class OrganizationResponse(OrganizationBase):
    """Schema for organization response"""
    id: int
    plan: str
    is_active: bool
    max_users: int
    max_api_keys: int
    settings: Dict[str, Any]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class MessageResponse(BaseModel):
    """Generic message response"""
    message: str
