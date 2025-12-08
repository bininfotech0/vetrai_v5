"""
Database models for API Keys Service
"""
import sys
from pathlib import Path
from datetime import datetime

sys.path.append(str(Path(__file__).parent.parent.parent))

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, JSON
from shared.models import BaseModel


class APIKey(BaseModel):
    """API key model"""
    
    __tablename__ = "api_keys"
    
    name = Column(String(100), nullable=False)
    key_hash = Column(String(255), nullable=False, unique=True, index=True)
    key_prefix = Column(String(20), nullable=False, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    organization_id = Column(Integer, nullable=False, index=True)
    
    scopes = Column(JSON, nullable=False, default=list)
    rate_limit = Column(Integer, nullable=True)  # requests per minute
    
    is_active = Column(Boolean, default=True, nullable=False)
    expires_at = Column(DateTime, nullable=True)
    last_used_at = Column(DateTime, nullable=True)
    
    def __repr__(self):
        return f"<APIKey(id={self.id}, name='{self.name}', prefix='{self.key_prefix}')>"


class APIKeyUsage(BaseModel):
    """API key usage tracking"""
    
    __tablename__ = "api_key_usage"
    
    api_key_id = Column(Integer, nullable=False, index=True)
    endpoint = Column(String(255), nullable=False)
    method = Column(String(10), nullable=False)
    status_code = Column(Integer, nullable=False)
    response_time_ms = Column(Integer, nullable=True)
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(String(500), nullable=True)
    
    def __repr__(self):
        return f"<APIKeyUsage(id={self.id}, api_key_id={self.api_key_id})>"
