"""
API routes for API Keys Service
"""

import hashlib
import secrets
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import List

sys.path.append(str(Path(__file__).parent.parent.parent))

from fastapi import APIRouter, Depends, HTTPException, status
from shared.config import get_settings
from shared.middleware import CurrentUser, get_current_user
from shared.utils import get_db
from sqlalchemy.orm import Session

from .models import APIKey
from .schemas import (APIKeyCreate, APIKeyCreateResponse, APIKeyResponse,
                      APIKeyUpdate, APIKeyUsageStats, MessageResponse)

router = APIRouter()
settings = get_settings()


def generate_api_key() -> tuple[str, str, str]:
    """
    Generate a new API key with prefix and hash

    Returns:
        Tuple of (full_key, key_prefix, key_hash)
    """
    # Generate random key
    random_part = secrets.token_urlsafe(settings.api_key_length)
    full_key = f"{settings.api_key_prefix}{random_part}"

    # Create prefix (first 8 characters for display)
    key_prefix = full_key[:8] + "..." + full_key[-4:]

    # Hash the key for storage
    key_hash = hashlib.sha256(full_key.encode()).hexdigest()

    return full_key, key_prefix, key_hash


@router.post(
    "/keys", response_model=APIKeyCreateResponse, status_code=status.HTTP_201_CREATED
)
async def create_api_key(
    key_data: APIKeyCreate,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Create a new API key"""

    # Generate API key
    full_key, key_prefix, key_hash = generate_api_key()

    # Calculate expiration
    expires_at = None
    if key_data.expires_days:
        expires_at = datetime.utcnow() + timedelta(days=key_data.expires_days)

    # Create API key record
    api_key = APIKey(
        organization_id=current_user.organization_id,
        user_id=current_user.user_id,
        name=key_data.name,
        key_hash=key_hash,
        key_prefix=key_prefix,
        scopes=key_data.scopes,
        expires_at=expires_at,
    )

    db.add(api_key)
    db.commit()
    db.refresh(api_key)

    # Return response with full key (only time it's shown)
    response_data = APIKeyResponse.model_validate(api_key).model_dump()
    response_data["key"] = full_key

    return APIKeyCreateResponse(**response_data)


@router.get("/keys", response_model=List[APIKeyResponse])
async def list_api_keys(
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
):
    """List user's API keys (masked)"""

    query = db.query(APIKey).filter(
        APIKey.organization_id == current_user.organization_id,
        APIKey.user_id == current_user.user_id,
    )

    keys = query.offset(skip).limit(limit).all()
    return keys


@router.get("/keys/{key_id}", response_model=APIKeyResponse)
async def get_api_key(
    key_id: int,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get API key details (masked)"""

    key = (
        db.query(APIKey)
        .filter(
            APIKey.id == key_id,
            APIKey.organization_id == current_user.organization_id,
            APIKey.user_id == current_user.user_id,
        )
        .first()
    )

    if not key:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="API key not found"
        )

    return key


@router.put("/keys/{key_id}", response_model=APIKeyResponse)
async def update_api_key(
    key_id: int,
    key_update: APIKeyUpdate,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Update API key scopes/expiry"""

    key = (
        db.query(APIKey)
        .filter(
            APIKey.id == key_id,
            APIKey.organization_id == current_user.organization_id,
            APIKey.user_id == current_user.user_id,
        )
        .first()
    )

    if not key:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="API key not found"
        )

    # Update fields
    if key_update.name is not None:
        key.name = key_update.name
    if key_update.scopes is not None:
        key.scopes = key_update.scopes
    if key_update.is_active is not None:
        key.is_active = key_update.is_active
    if key_update.expires_at is not None:
        key.expires_at = key_update.expires_at

    db.commit()
    db.refresh(key)

    return key


@router.delete("/keys/{key_id}", response_model=MessageResponse)
async def delete_api_key(
    key_id: int,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Revoke/delete API key"""

    key = (
        db.query(APIKey)
        .filter(
            APIKey.id == key_id,
            APIKey.organization_id == current_user.organization_id,
            APIKey.user_id == current_user.user_id,
        )
        .first()
    )

    if not key:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="API key not found"
        )

    # Soft delete by deactivating
    key.is_active = False
    db.commit()

    return {"message": "API key revoked successfully"}


@router.get("/keys/{key_id}/usage", response_model=APIKeyUsageStats)
async def get_api_key_usage(
    key_id: int,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get API key usage statistics"""

    key = (
        db.query(APIKey)
        .filter(
            APIKey.id == key_id,
            APIKey.organization_id == current_user.organization_id,
            APIKey.user_id == current_user.user_id,
        )
        .first()
    )

    if not key:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="API key not found"
        )

    # Return basic stats from API key model
    # In production, you'd query api_key_usage table for detailed stats
    return {
        "total_requests": key.usage_count,
        "success_requests": key.usage_count,  # Placeholder
        "failed_requests": 0,  # Placeholder
        "avg_response_time_ms": 0.0,  # Placeholder
        "requests_by_endpoint": {},  # Placeholder
    }
