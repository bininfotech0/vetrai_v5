"""
Database models for Notifications Service
"""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from shared.models import BaseModel
from sqlalchemy import JSON, Boolean, Column, DateTime, Integer, String, Text


class Notification(BaseModel):
    """Notification model"""

    __tablename__ = "notifications"

    user_id = Column(Integer, nullable=False, index=True)
    organization_id = Column(Integer, nullable=False, index=True)
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    type = Column(String(50), nullable=False)
    channel = Column(String(50), nullable=False)
    is_read = Column(Boolean, default=False, index=True)
    read_at = Column(DateTime, nullable=True)
    metadata = Column(JSON, default=dict)

    def __repr__(self):
        return f"<Notification(id={self.id}, title='{self.title}', user_id={self.user_id})>"


class NotificationTemplate(BaseModel):
    """Notification template model"""

    __tablename__ = "notification_templates"

    name = Column(String(255), unique=True, nullable=False, index=True)
    subject = Column(String(500), nullable=False)
    html_content = Column(Text, nullable=False)
    text_content = Column(Text, nullable=False)
    variables = Column(JSON, default=list)
    is_active = Column(Boolean, nullable=False, default=True, index=True)

    def __repr__(self):
        return f"<NotificationTemplate(id={self.id}, name='{self.name}')>"
