"""
API routes for Notifications Service
"""
import sys
from pathlib import Path
from typing import List

sys.path.append(str(Path(__file__).parent.parent.parent))

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from shared.utils import get_db
from shared.middleware import CurrentUser, get_current_user, require_org_admin
from shared.config import get_settings

from models import Notification, NotificationTemplate, NotificationStatus
from schemas import (
    NotificationCreate,
    NotificationResponse,
    TemplateCreate,
    TemplateUpdate,
    TemplateResponse,
    MessageResponse,
)

router = APIRouter()
settings = get_settings()


@router.post("/", response_model=NotificationResponse, status_code=status.HTTP_201_CREATED)
async def create_notification(
    notification_data: NotificationCreate,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create and send a notification"""
    
    notification = Notification(
        user_id=current_user.user_id,
        organization_id=current_user.organization_id,
        type=notification_data.type,
        subject=notification_data.subject,
        message=notification_data.message,
        recipient=notification_data.recipient,
        extra_data=notification_data.extra_data
    )
    
    db.add(notification)
    db.commit()
    db.refresh(notification)
    
    # TODO: Queue notification for sending via Redis
    # TODO: Send notification via appropriate channel
    
    return notification


@router.get("/", response_model=List[NotificationResponse])
async def list_notifications(
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
    status_filter: str = None,
    skip: int = 0,
    limit: int = 100
):
    """List notifications for current user"""
    
    query = db.query(Notification).filter(
        Notification.user_id == current_user.user_id
    )
    
    if status_filter:
        query = query.filter(Notification.status == status_filter)
    
    notifications = query.offset(skip).limit(limit).all()
    return notifications


@router.get("/{notification_id}", response_model=NotificationResponse)
async def get_notification(
    notification_id: int,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get notification by ID"""
    
    notification = db.query(Notification).filter(
        Notification.id == notification_id,
        Notification.user_id == current_user.user_id
    ).first()
    
    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found"
        )
    
    return notification


@router.post("/templates", response_model=TemplateResponse, status_code=status.HTTP_201_CREATED)
async def create_template(
    template_data: TemplateCreate,
    current_user: CurrentUser = Depends(require_org_admin()),
    db: Session = Depends(get_db)
):
    """Create a notification template"""
    
    # Check if template with same name exists
    existing = db.query(NotificationTemplate).filter(
        NotificationTemplate.name == template_data.name
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Template with this name already exists"
        )
    
    template = NotificationTemplate(
        organization_id=current_user.organization_id,
        name=template_data.name,
        type=template_data.type,
        subject=template_data.subject,
        body=template_data.body
    )
    
    db.add(template)
    db.commit()
    db.refresh(template)
    
    return template


@router.get("/templates", response_model=List[TemplateResponse])
async def list_templates(
    current_user: CurrentUser = Depends(require_org_admin()),
    db: Session = Depends(get_db)
):
    """List notification templates"""
    
    templates = db.query(NotificationTemplate).filter(
        (NotificationTemplate.organization_id == current_user.organization_id) |
        (NotificationTemplate.organization_id.is_(None))
    ).all()
    
    return templates


@router.get("/templates/{template_id}", response_model=TemplateResponse)
async def get_template(
    template_id: int,
    current_user: CurrentUser = Depends(require_org_admin()),
    db: Session = Depends(get_db)
):
    """Get template by ID"""
    
    template = db.query(NotificationTemplate).filter(
        NotificationTemplate.id == template_id
    ).first()
    
    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Template not found"
        )
    
    # Check access
    if template.organization_id and template.organization_id != current_user.organization_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    return template


@router.put("/templates/{template_id}", response_model=TemplateResponse)
async def update_template(
    template_id: int,
    template_update: TemplateUpdate,
    current_user: CurrentUser = Depends(require_org_admin()),
    db: Session = Depends(get_db)
):
    """Update notification template"""
    
    template = db.query(NotificationTemplate).filter(
        NotificationTemplate.id == template_id,
        NotificationTemplate.organization_id == current_user.organization_id
    ).first()
    
    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Template not found"
        )
    
    # Update fields
    if template_update.subject is not None:
        template.subject = template_update.subject
    if template_update.body is not None:
        template.body = template_update.body
    if template_update.is_active is not None:
        template.is_active = template_update.is_active
    
    db.commit()
    db.refresh(template)
    
    return template


@router.delete("/templates/{template_id}", response_model=MessageResponse)
async def delete_template(
    template_id: int,
    current_user: CurrentUser = Depends(require_org_admin()),
    db: Session = Depends(get_db)
):
    """Delete notification template"""
    
    template = db.query(NotificationTemplate).filter(
        NotificationTemplate.id == template_id,
        NotificationTemplate.organization_id == current_user.organization_id
    ).first()
    
    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Template not found"
        )
    
    db.delete(template)
    db.commit()
    
    return {"message": "Template deleted successfully"}
