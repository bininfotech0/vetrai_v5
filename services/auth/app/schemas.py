"""
Pydantic schemas for Authentication Service
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class UserRole:
    """User role constants"""
    SUPER_ADMIN = "super_admin"
    ORG_ADMIN = "org_admin"
    USER = "user"
    SUPPORT_AGENT = "support_agent"
    BILLING_ADMIN = "billing_admin"


class UserBase(BaseModel):
    """Base user schema"""
    email: EmailStr
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)


class UserCreate(UserBase):
    """Schema for creating a new user"""
    password: str = Field(..., min_length=8)
    organization_id: int
    role: str = UserRole.USER


class UserUpdate(BaseModel):
    """Schema for updating a user"""
    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)
    is_active: Optional[bool] = None
    role: Optional[str] = None


class UserResponse(UserBase):
    """Schema for user response"""
    id: int
    role: str
    organization_id: int
    is_active: bool
    is_verified: bool
    created_at: datetime
    last_login: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class LoginRequest(BaseModel):
    """Schema for login request"""
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    """Schema for login response"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: UserResponse


class TokenRefreshRequest(BaseModel):
    """Schema for token refresh request"""
    refresh_token: str


class TokenRefreshResponse(BaseModel):
    """Schema for token refresh response"""
    access_token: str
    token_type: str = "bearer"


class PasswordChangeRequest(BaseModel):
    """Schema for password change request"""
    old_password: str
    new_password: str = Field(..., min_length=8)


class PasswordResetRequest(BaseModel):
    """Schema for password reset request"""
    email: EmailStr


class PasswordResetConfirm(BaseModel):
    """Schema for password reset confirmation"""
    token: str
    new_password: str = Field(..., min_length=8)


class VerifyEmailRequest(BaseModel):
    """Schema for email verification"""
    token: str


class MessageResponse(BaseModel):
    """Generic message response"""
    message: str
