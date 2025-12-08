"""
Pydantic schemas for Notifications Service
"""

from datetime import datetime
from typing import Dict, Optional

from pydantic import BaseModel, Field


class NotificationCreate(BaseModel):
    """Schema for creating a notification"""

    user_id: int
    title: str = Field(..., min_length=1, max_length=255)
    message: str = Field(..., min_length=1)
    type: str = Field(..., description="Type of notification")
    channel: str = Field(..., description="Channel (email, in_app, sms)")
    metadata: Optional[Dict] = {}


class NotificationResponse(BaseModel):
    """Schema for notification response"""

    id: int
    user_id: int
    organization_id: int
    title: str
    message: str
    type: str
    channel: str
    is_read: bool
    read_at: Optional[datetime]
    created_at: datetime

    class Config:
        from_attributes = True


class NotificationPreferences(BaseModel):
    """Schema for notification preferences"""

    email_enabled: bool = True
    in_app_enabled: bool = True
    sms_enabled: bool = False


class MessageResponse(BaseModel):
    """Generic message response"""

    message: str
