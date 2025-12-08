"""
Database models for Themes Service
"""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from shared.models import BaseModel
from sqlalchemy import Boolean, Column, Integer, String, Text


class Theme(BaseModel):
    """Theme model for organization branding"""

    __tablename__ = "themes"

    organization_id = Column(Integer, nullable=False, unique=True, index=True)
    name = Column(String(255), nullable=False)
    logo_url = Column(String(500), nullable=True)
    favicon_url = Column(String(500), nullable=True)
    primary_color = Column(String(20), nullable=True)
    secondary_color = Column(String(20), nullable=True)
    accent_color = Column(String(20), nullable=True)
    custom_css = Column(Text, nullable=True)
    custom_js = Column(Text, nullable=True)
    is_active = Column(Boolean, nullable=False, default=True, index=True)

    def __repr__(self):
        return f"<Theme(id={self.id}, organization_id={self.organization_id}, name='{self.name}')>"
