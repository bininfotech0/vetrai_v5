"""
Pydantic schemas for Themes Service
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ThemeUpdate(BaseModel):
    """Schema for updating theme"""

    name: Optional[str] = None
    primary_color: Optional[str] = None
    secondary_color: Optional[str] = None
    accent_color: Optional[str] = None
    custom_css: Optional[str] = None
    custom_js: Optional[str] = None


class ThemeResponse(BaseModel):
    """Schema for theme response"""

    id: int
    organization_id: int
    name: str
    logo_url: Optional[str]
    favicon_url: Optional[str]
    primary_color: Optional[str]
    secondary_color: Optional[str]
    accent_color: Optional[str]
    custom_css: Optional[str]
    custom_js: Optional[str]
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class MessageResponse(BaseModel):
    """Generic message response"""

    message: str
