"""
Database models for API Keys Service
"""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from shared.models import BaseModel
from sqlalchemy import JSON, Boolean, Column, DateTime, Integer, String


class APIKey(BaseModel):
    """API Key model for secure key management"""

    __tablename__ = "api_keys"

    organization_id = Column(Integer, nullable=False, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    key_hash = Column(String(255), nullable=False, unique=True, index=True)
    key_prefix = Column(String(20), nullable=False)
    scopes = Column(JSON, default=list, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False, index=True)
    expires_at = Column(DateTime, nullable=True)
    last_used_at = Column(DateTime, nullable=True)
    usage_count = Column(Integer, default=0, nullable=False)

    def __repr__(self):
        return f"<APIKey(id={self.id}, name='{self.name}', organization_id={self.organization_id})>"
