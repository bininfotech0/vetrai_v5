"""
Multi-tenancy middleware for VetrAI Platform
"""
from typing import Optional

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from .auth import CurrentUser, get_current_user
from ..utils import get_db


class TenantContext:
    """Tenant context for multi-tenant operations"""
    
    def __init__(
        self,
        organization_id: int,
        user: CurrentUser,
        db: Session
    ):
        self.organization_id = organization_id
        self.user = user
        self.db = db
    
    def verify_access(self, resource_org_id: Optional[int]) -> None:
        """
        Verify that user has access to resource from their organization
        
        Args:
            resource_org_id: Organization ID of the resource
        
        Raises:
            HTTPException: If user doesn't have access
        """
        if resource_org_id is None:
            return
        
        # Super admins can access all resources
        if self.user.is_super_admin():
            return
        
        # Check if resource belongs to user's organization
        if resource_org_id != self.organization_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied to resource from different organization"
            )
    
    def apply_tenant_filter(self, query):
        """
        Apply tenant filter to SQLAlchemy query
        
        Args:
            query: SQLAlchemy query object
        
        Returns:
            Filtered query
        """
        # Super admins see all data
        if self.user.is_super_admin():
            return query
        
        # Filter by organization_id
        return query.filter_by(organization_id=self.organization_id)


async def get_tenant_context(
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> TenantContext:
    """
    Get tenant context for current user
    
    Args:
        current_user: Current authenticated user
        db: Database session
    
    Returns:
        TenantContext instance
    """
    return TenantContext(
        organization_id=current_user.organization_id,
        user=current_user,
        db=db
    )
