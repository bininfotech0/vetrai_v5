"""
API routes for Tenancy Service
"""
import sys
from pathlib import Path
from typing import List

sys.path.append(str(Path(__file__).parent.parent.parent))

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from shared.utils import get_db
from shared.middleware import CurrentUser, get_current_user, require_super_admin, require_org_admin

from models import Organization
from schemas import (
    OrganizationCreate,
    OrganizationUpdate,
    OrganizationResponse,
    MessageResponse,
)

router = APIRouter()


@router.post("/organizations", response_model=OrganizationResponse, status_code=status.HTTP_201_CREATED)
async def create_organization(
    org_data: OrganizationCreate,
    current_user: CurrentUser = Depends(require_super_admin()),
    db: Session = Depends(get_db)
):
    """Create a new organization (super admin only)"""
    
    # Check if slug already exists
    existing_org = db.query(Organization).filter(Organization.slug == org_data.slug).first()
    if existing_org:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Organization slug already exists"
        )
    
    # Create organization
    org = Organization(
        name=org_data.name,
        slug=org_data.slug,
        domain=org_data.domain,
        plan=org_data.plan,
        max_users=org_data.max_users,
        max_api_keys=org_data.max_api_keys,
        settings=org_data.settings
    )
    
    db.add(org)
    db.commit()
    db.refresh(org)
    
    return org


@router.get("/organizations", response_model=List[OrganizationResponse])
async def list_organizations(
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    """List organizations"""
    
    query = db.query(Organization)
    
    # Non-super admins can only see their own organization
    if not current_user.is_super_admin():
        query = query.filter(Organization.id == current_user.organization_id)
    
    orgs = query.offset(skip).limit(limit).all()
    return orgs


@router.get("/organizations/{org_id}", response_model=OrganizationResponse)
async def get_organization(
    org_id: int,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get organization by ID"""
    
    org = db.query(Organization).filter(Organization.id == org_id).first()
    if not org:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found"
        )
    
    # Non-super admins can only view their own organization
    if not current_user.is_super_admin() and org.id != current_user.organization_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    return org


@router.put("/organizations/{org_id}", response_model=OrganizationResponse)
async def update_organization(
    org_id: int,
    org_update: OrganizationUpdate,
    current_user: CurrentUser = Depends(require_org_admin()),
    db: Session = Depends(get_db)
):
    """Update organization"""
    
    org = db.query(Organization).filter(Organization.id == org_id).first()
    if not org:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found"
        )
    
    # Non-super admins can only update their own organization
    if not current_user.is_super_admin() and org.id != current_user.organization_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    # Update fields
    if org_update.name is not None:
        org.name = org_update.name
    if org_update.domain is not None:
        org.domain = org_update.domain
    if org_update.plan is not None and current_user.is_super_admin():
        org.plan = org_update.plan
    if org_update.is_active is not None and current_user.is_super_admin():
        org.is_active = org_update.is_active
    if org_update.max_users is not None and current_user.is_super_admin():
        org.max_users = org_update.max_users
    if org_update.max_api_keys is not None and current_user.is_super_admin():
        org.max_api_keys = org_update.max_api_keys
    if org_update.settings is not None:
        org.settings = org_update.settings
    
    db.commit()
    db.refresh(org)
    
    return org


@router.delete("/organizations/{org_id}", response_model=MessageResponse)
async def delete_organization(
    org_id: int,
    current_user: CurrentUser = Depends(require_super_admin()),
    db: Session = Depends(get_db)
):
    """Delete organization (super admin only)"""
    
    org = db.query(Organization).filter(Organization.id == org_id).first()
    if not org:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found"
        )
    
    db.delete(org)
    db.commit()
    
    return {"message": "Organization deleted successfully"}
