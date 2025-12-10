"""
Pydantic schemas for Notifications Service
"""
from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field


class NotificationCreate(BaseModel):
    """Schema for creating a notification"""
    type: str
    subject: Optional[str] = None
    message: str = Field(..., min_length=1)
    recipient: str = Field(..., min_length=1)
    extra_data: Optional[Dict[str, Any]] = None


class NotificationResponse(BaseModel):
    """Schema for notification response"""
    id: int
    user_id: int
    organization_id: int
    type: str
    status: str
    subject: Optional[str]
    message: str
    recipient: str
    sender: Optional[str]
    extra_data: Optional[Dict[str, Any]]
    error_message: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True


class TemplateCreate(BaseModel):
    """Schema for creating a notification template"""
    name: str = Field(..., min_length=1, max_length=100)
    type: str
    subject: Optional[str] = None
    body: str = Field(..., min_length=1)


class TemplateUpdate(BaseModel):
    """Schema for updating a notification template"""
    subject: Optional[str] = None
    body: Optional[str] = None
    is_active: Optional[bool] = None


class TemplateResponse(BaseModel):
    """Schema for template response"""
    id: int
    organization_id: Optional[int]
    name: str
    type: str
    subject: Optional[str]
    body: str
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class MessageResponse(BaseModel):
    """Generic message response"""
    message: str
