"""
Database models for Authentication Service
"""
import sys
from pathlib import Path
from datetime import datetime

sys.path.append(str(Path(__file__).parent.parent.parent))

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum as SQLEnum
from shared.models import BaseModel
import enum


class UserRole(enum.Enum):
    """User role enumeration"""
    SUPER_ADMIN = "super_admin"
    ORG_ADMIN = "org_admin"
    USER = "user"
    SUPPORT_AGENT = "support_agent"
    BILLING_ADMIN = "billing_admin"


class User(BaseModel):
    """User model"""
    
    __tablename__ = "users"
    
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    role = Column(SQLEnum(UserRole), nullable=False, default=UserRole.USER)
    organization_id = Column(Integer, nullable=False, index=True)
    
    is_active = Column(Boolean, default=True, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    
    last_login = Column(DateTime, nullable=True)
    verification_token = Column(String(255), nullable=True)
    verification_token_expires = Column(DateTime, nullable=True)
    password_reset_token = Column(String(255), nullable=True)
    password_reset_expires = Column(DateTime, nullable=True)
    
    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}', role='{self.role.value}')>"


class RefreshToken(BaseModel):
    """Refresh token model for JWT token management"""
    
    __tablename__ = "refresh_tokens"
    
    user_id = Column(Integer, nullable=False, index=True)
    token = Column(String(500), nullable=False, unique=True, index=True)
    expires_at = Column(DateTime, nullable=False)
    is_revoked = Column(Boolean, default=False, nullable=False)
    revoked_at = Column(DateTime, nullable=True)
    
    def __repr__(self):
        return f"<RefreshToken(id={self.id}, user_id={self.user_id})>"


class AuditLog(BaseModel):
    """Audit log for tracking user activities"""
    
    __tablename__ = "audit_logs"
    
    user_id = Column(Integer, nullable=True, index=True)
    organization_id = Column(Integer, nullable=True, index=True)
    action = Column(String(100), nullable=False)
    resource_type = Column(String(50), nullable=True)
    resource_id = Column(Integer, nullable=True)
    details = Column(String(1000), nullable=True)
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(String(500), nullable=True)
    
    def __repr__(self):
        return f"<AuditLog(id={self.id}, action='{self.action}', user_id={self.user_id})>"
