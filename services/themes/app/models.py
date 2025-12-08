"""
Database models for Themes Service
"""
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from sqlalchemy import Column, Integer, String, Text, Boolean, JSON
from shared.models import BaseModel


class Theme(BaseModel):
    """Theme model"""
    
    __tablename__ = "themes"
    
    organization_id = Column(Integer, nullable=False, unique=True, index=True)
    name = Column(String(100), nullable=False)
    
    # Colors
    primary_color = Column(String(7), nullable=False, default="#1976d2")
    secondary_color = Column(String(7), nullable=False, default="#424242")
    accent_color = Column(String(7), nullable=False, default="#82b1ff")
    
    # Logo
    logo_url = Column(String(500), nullable=True)
    favicon_url = Column(String(500), nullable=True)
    
    # Custom CSS
    custom_css = Column(Text, nullable=True)
    
    # Additional settings
    settings = Column(JSON, nullable=True, default=dict)
    
    is_active = Column(Boolean, default=True, nullable=False)
    
    def __repr__(self):
        return f"<Theme(id={self.id}, org_id={self.organization_id}, name='{self.name}')>"


class PublicPage(BaseModel):
    """Public page content model"""
    
    __tablename__ = "public_pages"
    
    organization_id = Column(Integer, nullable=False, index=True)
    slug = Column(String(100), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    
    is_published = Column(Boolean, default=False, nullable=False)
    
    def __repr__(self):
        return f"<PublicPage(id={self.id}, slug='{self.slug}')>"
