"""
Pydantic schemas for Themes Service
"""
from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field


class ThemeCreate(BaseModel):
    """Schema for creating a theme"""
    name: str = Field(..., min_length=1, max_length=100)
    primary_color: str = "#1976d2"
    secondary_color: str = "#424242"
    accent_color: str = "#82b1ff"
    custom_css: Optional[str] = None
    settings: Optional[Dict[str, Any]] = None


class ThemeUpdate(BaseModel):
    """Schema for updating a theme"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    primary_color: Optional[str] = None
    secondary_color: Optional[str] = None
    accent_color: Optional[str] = None
    logo_url: Optional[str] = None
    favicon_url: Optional[str] = None
    custom_css: Optional[str] = None
    settings: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None


class ThemeResponse(BaseModel):
    """Schema for theme response"""
    id: int
    organization_id: int
    name: str
    primary_color: str
    secondary_color: str
    accent_color: str
    logo_url: Optional[str]
    favicon_url: Optional[str]
    custom_css: Optional[str]
    settings: Optional[Dict[str, Any]]
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class PublicPageCreate(BaseModel):
    """Schema for creating a public page"""
    slug: str = Field(..., min_length=1, max_length=100)
    title: str = Field(..., min_length=1, max_length=255)
    content: str = Field(..., min_length=1)


class PublicPageUpdate(BaseModel):
    """Schema for updating a public page"""
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    content: Optional[str] = None
    is_published: Optional[bool] = None


class PublicPageResponse(BaseModel):
    """Schema for public page response"""
    id: int
    organization_id: int
    slug: str
    title: str
    content: str
    is_published: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class MessageResponse(BaseModel):
    """Generic message response"""
    message: str
