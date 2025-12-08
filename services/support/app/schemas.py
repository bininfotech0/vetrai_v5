"""
Pydantic schemas for Support Service
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class TicketCreate(BaseModel):
    """Schema for creating a ticket"""

    title: str = Field(..., min_length=1, max_length=255)
    description: str = Field(..., min_length=1)
    priority: str = Field(default="medium")
    category: Optional[str] = None


class TicketUpdate(BaseModel):
    """Schema for updating a ticket"""

    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    assigned_to: Optional[int] = None


class TicketResponse(BaseModel):
    """Schema for ticket response"""

    id: int
    organization_id: int
    user_id: int
    assigned_to: Optional[int]
    title: str
    description: str
    status: str
    priority: str
    category: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CommentCreate(BaseModel):
    """Schema for creating a comment"""

    comment: str = Field(..., min_length=1)
    is_internal: bool = False


class CommentResponse(BaseModel):
    """Schema for comment response"""

    id: int
    ticket_id: int
    user_id: int
    comment: str
    is_internal: bool
    created_at: datetime

    class Config:
        from_attributes = True


class MessageResponse(BaseModel):
    """Generic message response"""

    message: str
