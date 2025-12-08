"""
Authentication middleware for VetrAI Platform
"""
from typing import Optional, List
from enum import Enum

from fastapi import Depends, HTTPException, status, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from ..utils import decode_token, get_db


class UserRole(str, Enum):
    """User roles for RBAC"""
    SUPER_ADMIN = "super_admin"
    ORG_ADMIN = "org_admin"
    USER = "user"
    SUPPORT_AGENT = "support_agent"
    BILLING_ADMIN = "billing_admin"


security = HTTPBearer()


class CurrentUser:
    """Current authenticated user information"""
    
    def __init__(
        self,
        user_id: int,
        email: str,
        organization_id: int,
        role: UserRole,
        is_active: bool = True
    ):
        self.user_id = user_id
        self.email = email
        self.organization_id = organization_id
        self.role = role
        self.is_active = is_active
    
    def has_role(self, *roles: UserRole) -> bool:
        """Check if user has one of the specified roles"""
        return self.role in roles
    
    def is_super_admin(self) -> bool:
        """Check if user is super admin"""
        return self.role == UserRole.SUPER_ADMIN
    
    def is_org_admin(self) -> bool:
        """Check if user is organization admin"""
        return self.role in [UserRole.SUPER_ADMIN, UserRole.ORG_ADMIN]


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> CurrentUser:
    """
    Get current authenticated user from JWT token
    
    Args:
        credentials: HTTP Bearer credentials
        db: Database session
    
    Returns:
        CurrentUser instance
    
    Raises:
        HTTPException: If token is invalid or user not found
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    token = credentials.credentials
    payload = decode_token(token)
    
    if payload is None:
        raise credentials_exception
    
    user_id: Optional[int] = payload.get("sub")
    if user_id is None:
        raise credentials_exception
    
    # Extract user info from token
    email = payload.get("email")
    organization_id = payload.get("organization_id")
    role = payload.get("role", UserRole.USER)
    is_active = payload.get("is_active", True)
    
    if not is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )
    
    return CurrentUser(
        user_id=user_id,
        email=email,
        organization_id=organization_id,
        role=UserRole(role),
        is_active=is_active
    )


async def get_optional_user(
    authorization: Optional[str] = Header(None)
) -> Optional[CurrentUser]:
    """
    Get current user if authenticated, None otherwise
    
    Args:
        authorization: Authorization header
    
    Returns:
        CurrentUser instance or None
    """
    if not authorization or not authorization.startswith("Bearer "):
        return None
    
    try:
        token = authorization.replace("Bearer ", "")
        payload = decode_token(token)
        
        if payload is None:
            return None
        
        user_id = payload.get("sub")
        if user_id is None:
            return None
        
        return CurrentUser(
            user_id=user_id,
            email=payload.get("email"),
            organization_id=payload.get("organization_id"),
            role=UserRole(payload.get("role", UserRole.USER)),
            is_active=payload.get("is_active", True)
        )
    except Exception:
        return None


def require_roles(*roles: UserRole):
    """
    Dependency to require specific roles
    
    Usage:
        @app.get("/admin/")
        def admin_endpoint(
            current_user: CurrentUser = Depends(require_roles(UserRole.SUPER_ADMIN, UserRole.ORG_ADMIN))
        ):
            ...
    """
    async def role_checker(current_user: CurrentUser = Depends(get_current_user)) -> CurrentUser:
        if not current_user.has_role(*roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions"
            )
        return current_user
    
    return role_checker


def require_super_admin():
    """Dependency to require super admin role"""
    return require_roles(UserRole.SUPER_ADMIN)


def require_org_admin():
    """Dependency to require organization admin or super admin role"""
    return require_roles(UserRole.SUPER_ADMIN, UserRole.ORG_ADMIN)
