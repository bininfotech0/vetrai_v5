"""
Shared middleware for VetrAI Platform
"""
from .auth import (
    CurrentUser,
    UserRole,
    get_current_user,
    get_optional_user,
    require_roles,
    require_super_admin,
    require_org_admin,
)
from .tenant import TenantContext, get_tenant_context

__all__ = [
    # Auth
    "CurrentUser",
    "UserRole",
    "get_current_user",
    "get_optional_user",
    "require_roles",
    "require_super_admin",
    "require_org_admin",
    # Tenant
    "TenantContext",
    "get_tenant_context",
]
