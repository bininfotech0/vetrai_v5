"""
Database models for Notifications Service
"""
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from sqlalchemy import Column, Integer, String, Text, Boolean, Enum as SQLEnum, JSON
from shared.models import BaseModel
import enum


class NotificationType(enum.Enum):
    """Notification type enumeration"""
    EMAIL = "email"
    SMS = "sms"
    IN_APP = "in_app"
    PUSH = "push"


class NotificationStatus(enum.Enum):
    """Notification status enumeration"""
    PENDING = "pending"
    SENT = "sent"
    FAILED = "failed"
    DELIVERED = "delivered"


class Notification(BaseModel):
    """Notification model"""
    
    __tablename__ = "notifications"
    
    user_id = Column(Integer, nullable=False, index=True)
    organization_id = Column(Integer, nullable=False, index=True)
    
    type = Column(SQLEnum(NotificationType), nullable=False)
    status = Column(SQLEnum(NotificationStatus), nullable=False, default=NotificationStatus.PENDING)
    
    subject = Column(String(255), nullable=True)
    message = Column(Text, nullable=False)
    
    recipient = Column(String(255), nullable=False)
    sender = Column(String(255), nullable=True)
    
    extra_data = Column(JSON, nullable=True, default=dict)
    error_message = Column(Text, nullable=True)
    
    def __repr__(self):
        return f"<Notification(id={self.id}, type='{self.type.value}', status='{self.status.value}')>"


class NotificationTemplate(BaseModel):
    """Notification template model"""
    
    __tablename__ = "notification_templates"
    
    organization_id = Column(Integer, nullable=True, index=True)
    name = Column(String(100), nullable=False, unique=True, index=True)
    type = Column(SQLEnum(NotificationType), nullable=False)
    
    subject = Column(String(255), nullable=True)
    body = Column(Text, nullable=False)
    
    is_active = Column(Boolean, default=True, nullable=False)
    
    def __repr__(self):
        return f"<NotificationTemplate(id={self.id}, name='{self.name}', type='{self.type.value}')>"
