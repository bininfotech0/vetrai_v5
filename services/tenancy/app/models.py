"""
Database models for Tenancy Service
"""
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from sqlalchemy import Column, Integer, String, Boolean, JSON
from shared.models import BaseModel


class Organization(BaseModel):
    """Organization model"""
    
    __tablename__ = "organizations"
    
    name = Column(String(255), nullable=False)
    slug = Column(String(100), unique=True, nullable=False, index=True)
    domain = Column(String(255), nullable=True)
    plan = Column(String(50), nullable=False, default="free")
    is_active = Column(Boolean, default=True, nullable=False)
    max_users = Column(Integer, default=5)
    max_api_keys = Column(Integer, default=10)
    settings = Column(JSON, default={})
    
    def __repr__(self):
        return f"<Organization(id={self.id}, name='{self.name}', plan='{self.plan}')>"
