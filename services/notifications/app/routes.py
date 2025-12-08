"""
API routes for Notifications Service
"""
import sys
from datetime import datetime
from pathlib import Path
from typing import List
from typing import Optional

sys.path.append(str(Path(__file__).parent.parent.parent))

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from shared.utils import get_db
from shared.middleware import CurrentUser, get_current_user
from shared.config import get_settings

from .models import Notification
from .schemas import (
    NotificationCreate,
    NotificationResponse,
    NotificationPreferences,
    MessageResponse,
)

router = APIRouter()
settings = get_settings()


@router.post("/notifications", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
async def send_notification(
    notification_data: NotificationCreate,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Send notification"""
    notification = Notification(
        user_id=notification_data.user_id,
        organization_id=current_user.organization_id,
        title=notification_data.title,
        message=notification_data.message,
        type=notification_data.type,
        channel=notification_data.channel,
        metadata=notification_data.metadata
    )
    
    db.add(notification)
    db.commit()
    
    # TODO: Trigger actual notification sending (email/SMS)
    
    return {"message": "Notification sent successfully"}


@router.get("/notifications", response_model=List[NotificationResponse])
async def list_notifications(
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
    is_read: Optional[bool] = None,
    skip: int = 0,
    limit: int = 100
):
    """List user notifications"""
    query = db.query(Notification).filter(
        Notification.user_id == current_user.user_id
    )
    
    if is_read is not None:
        query = query.filter(Notification.is_read == is_read)
    
    notifications = query.order_by(Notification.created_at.desc()).offset(skip).limit(limit).all()
    return notifications


@router.put("/notifications/{notification_id}/read", response_model=MessageResponse)
async def mark_as_read(
    notification_id: int,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Mark notification as read"""
    notification = db.query(Notification).filter(
        Notification.id == notification_id,
        Notification.user_id == current_user.user_id
    ).first()
    
    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found"
        )
    
    notification.is_read = True
    notification.read_at = datetime.utcnow()
    db.commit()
    
    return {"message": "Notification marked as read"}


@router.get("/preferences", response_model=NotificationPreferences)
async def get_preferences(
    current_user: CurrentUser = Depends(get_current_user)
):
    """Get notification preferences"""
    # Placeholder - Return default preferences
    return {
        "email_enabled": True,
        "in_app_enabled": True,
        "sms_enabled": False
    }


@router.put("/preferences", response_model=MessageResponse)
async def update_preferences(
    preferences: NotificationPreferences,
    current_user: CurrentUser = Depends(get_current_user)
):
    """Update notification preferences"""
    # Placeholder - Store preferences
    return {"message": "Preferences updated successfully"}
