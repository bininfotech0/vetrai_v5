"""
API routes for API Keys Service
"""
import sys
from pathlib import Path
from datetime import datetime
from typing import List
import hashlib

sys.path.append(str(Path(__file__).parent.parent.parent))

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from shared.utils import get_db, generate_api_key
from shared.middleware import CurrentUser, get_current_user
from shared.config import get_settings

from .models import APIKey, APIKeyUsage
from .schemas import (
    APIKeyCreate,
    APIKeyUpdate,
    APIKeyResponse,
    APIKeyCreateResponse,
    APIKeyUsageResponse,
    MessageResponse,
)

router = APIRouter()
settings = get_settings()


def hash_api_key(key: str) -> str:
    """Hash an API key for storage"""
    return hashlib.sha256(key.encode()).hexdigest()


@router.post("/", response_model=APIKeyCreateResponse, status_code=status.HTTP_201_CREATED)
async def create_api_key(
    key_data: APIKeyCreate,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new API key"""
    
    # Generate API key
    full_key = generate_api_key()
    key_prefix = full_key[:12]
    key_hash = hash_api_key(full_key)
    
    # Create API key
    api_key = APIKey(
        name=key_data.name,
        key_hash=key_hash,
        key_prefix=key_prefix,
        user_id=current_user.user_id,
        organization_id=current_user.organization_id,
        scopes=key_data.scopes,
        rate_limit=key_data.rate_limit,
        expires_at=key_data.expires_at
    )
    
    db.add(api_key)
    db.commit()
    db.refresh(api_key)
    
    # Return response with full key (only time it's shown)
    response = APIKeyCreateResponse(
        id=api_key.id,
        name=api_key.name,
        key_prefix=api_key.key_prefix,
        user_id=api_key.user_id,
        organization_id=api_key.organization_id,
        scopes=api_key.scopes,
        rate_limit=api_key.rate_limit,
        is_active=api_key.is_active,
        expires_at=api_key.expires_at,
        last_used_at=api_key.last_used_at,
        created_at=api_key.created_at,
        key=full_key
    )
    
    return response


@router.get("/", response_model=List[APIKeyResponse])
async def list_api_keys(
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    """List API keys for current user's organization"""
    
    query = db.query(APIKey).filter(
        APIKey.organization_id == current_user.organization_id
    )
    
    api_keys = query.offset(skip).limit(limit).all()
    return api_keys


@router.get("/{key_id}", response_model=APIKeyResponse)
async def get_api_key(
    key_id: int,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get API key by ID"""
    
    api_key = db.query(APIKey).filter(
        APIKey.id == key_id,
        APIKey.organization_id == current_user.organization_id
    ).first()
    
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="API key not found"
        )
    
    return api_key


@router.put("/{key_id}", response_model=APIKeyResponse)
async def update_api_key(
    key_id: int,
    key_update: APIKeyUpdate,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update API key"""
    
    api_key = db.query(APIKey).filter(
        APIKey.id == key_id,
        APIKey.organization_id == current_user.organization_id
    ).first()
    
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="API key not found"
        )
    
    # Update fields
    if key_update.name is not None:
        api_key.name = key_update.name
    if key_update.scopes is not None:
        api_key.scopes = key_update.scopes
    if key_update.rate_limit is not None:
        api_key.rate_limit = key_update.rate_limit
    if key_update.is_active is not None:
        api_key.is_active = key_update.is_active
    
    db.commit()
    db.refresh(api_key)
    
    return api_key


@router.delete("/{key_id}", response_model=MessageResponse)
async def delete_api_key(
    key_id: int,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete API key"""
    
    api_key = db.query(APIKey).filter(
        APIKey.id == key_id,
        APIKey.organization_id == current_user.organization_id
    ).first()
    
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="API key not found"
        )
    
    db.delete(api_key)
    db.commit()
    
    return {"message": "API key deleted successfully"}


@router.get("/{key_id}/usage", response_model=List[APIKeyUsageResponse])
async def get_api_key_usage(
    key_id: int,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    """Get API key usage statistics"""
    
    # Verify API key belongs to user's organization
    api_key = db.query(APIKey).filter(
        APIKey.id == key_id,
        APIKey.organization_id == current_user.organization_id
    ).first()
    
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="API key not found"
        )
    
    usage = db.query(APIKeyUsage).filter(
        APIKeyUsage.api_key_id == key_id
    ).offset(skip).limit(limit).all()
    
    return usage
